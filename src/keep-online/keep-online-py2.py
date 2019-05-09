# -*- coding: utf-8 -*-
import re
import config
import requests
import urlparse

csu_url = "http://cloud.tencent.com/"
login_url = 'http://172.16.0.102/eportal/userV2.do'


def check_status():
    """
    通过心跳包监测网络连接状况
    :return: 网络状态，响应数据
    """
    result = requests.get(csu_url, allow_redirects=False)
    if result.status_code == 200:
        return "unavailable", result.text
    elif result.status_code == 301:
        return "available", ''
    else:
        return "exception", ''


def connect_network(location):
    """
    获取连接，自动补全帐号密码并登录
    :param location:
    :return: 连接结果
    """
    regex = re.match(r"<script>top.self.location.href='(.*)'</script>", location)
    if regex:
        # 解析登录参数
        location_url = regex.group(1)
        url_info = urlparse.urlparse(location_url)
        url_params = urlparse.parse_qs(url_info.query, True)
        # 开始登录网络
        url_params['method'] = 'login'
        url_params['param'] = 'true'
        http_data = {
            'is_auto_land': 'false',
            'usernameHidden': config.username,
            'username_tip': 'Username',
            'username': config.username,
            'pwd_tip': 'Password',
            'pwd': config.password
        }
        http_result = requests.post(login_url, params=url_params, data=http_data)
        if http_result.status_code == 200:
            return "success"
    return 'error'


if __name__ == '__main__':
    status, data = check_status()
    print('[INFO] 当前网络连接状态：{}'.format(status))
    if status == 'available':
        print('[INFO] 当前网络可以正常上网')
    elif status == 'unavailable':
        print('[RE] 正在尝试连接至校园网')
        result = connect_network(data)
        if result == 'success':
            print('[AC] 正在尝试连接至校园网')
        else:
            print('[WA] 重连失败，请稍后尝试')
    elif status == 'unavailable':
        print('[WA] 网络连接异常，请检查')

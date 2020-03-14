# coding=utf-8
import re
import time
import json
import requests
from my_config import user_list


def main():
    sign_user = set()
    while True:
        time_now = int(str_time("%H%M"))
        # 全新的一天
        if time_now >= 2358:
            sign_user = set()
            time.sleep(180)
            continue
        # 全部完成后不再自动尝试签到
        if len(sign_user) >= len(user_list):
            print("%s 今日已完工，明日自动继续" % str_time("%H:%M"))
            time.sleep(60)
            continue
        # 尝试进行签到
        for user in user_list:
            time.sleep(1)
            if user["username"] in sign_user:
                continue  # 忽略已完成签到人员

            print("正在为<%s>进行签到..." % user["username"], end="")
            if int(user["time"]) < time_now:
                sign_msg = sign_in(user)
                if sign_msg[0]:
                    sign_user.add(user["username"])
                    print("\033[0;32m成功\033[0m<{}>".format(sign_msg[1]))
                else:
                    print("\033[0;31m失败\033[0m<{}>".format(sign_msg[1]))
            else:
                print("\033[0;33m时间未到\033[0m<{}>".format(str_time("%H:%M")))
        time.sleep(1)


def sign_in(user_info):
    session = auto_login(user_info["username"], user_info["password"])
    if session is None:
        return False, "Get session failed"
    sign_result = auto_sign_in(session)
    if not isinstance(sign_result, dict):
        return False, sign_result
    elif sign_result["e"] == 0:
        return True, sign_result["m"]
    elif sign_result["e"] == 1 and sign_result["m"] == "今天已经填报了":
        return True, sign_result["m"]
    return False, sign_result["m"]


def auto_login(username, password):
    # 信息门户登录
    session = requests.Session()
    url = "http://ca.its.csu.edu.cn/Home/Login/215"
    http_data = {
        "userName": username,
        "passWord": password,
        "enter": "true"
    }
    try:
        http_result = session.post(url, data=http_data)
    except requests.exceptions.ReadTimeout:
        print("requests.exceptions.ReadTimeout:[%s]" % url)
        return None
    except requests.exceptions.ConnectionError:
        print("requests.exceptions.ConnectionError:[%s]" % url)
        return None
    regex = r'tokenId.*value="(?P<tokenId>\w+)".*account.*value="(?P<account>\w+)".*Thirdsys.*value="(?P<Thirdsys>\w+)"'
    re_result = re.search(regex, http_result.text)
    if re_result is None:
        return None

    # sso认证
    url = "https://wxxy.csu.edu.cn/a_csu/api/sso/validate"
    http_data = {
        "tokenId": re_result["tokenId"],
        "account": re_result["account"],
        "Thirdsys": re_result["Thirdsys"]
    }
    try:
        session.post(url, data=http_data)
    except requests.exceptions.ReadTimeout:
        print("requests.exceptions.ReadTimeout:[%s]" % url)
        return None
    except requests.exceptions.ConnectionError:
        print("requests.exceptions.ConnectionError:[%s]" % url)
        return None

    return session


def auto_sign_in(session):
    # 获取历史数据
    url = "https://wxxy.csu.edu.cn/ncov/wap/default/index"
    try:
        http_result = session.post(url)
    except requests.exceptions.ReadTimeout:
        print("requests.exceptions.ReadTimeout:[%s]" % url)
        return "自动登录失败"
    except requests.exceptions.ConnectionError:
        print("requests.exceptions.ConnectionError:[%s]" % url)
        return "自动登录失败"
    regex = r'oldInfo: (.*),'
    re_result = re.search(regex, http_result.text)
    if re_result is None:
        return "缺少历史数据"
    sign_data = json.loads(re_result.group(1))
    regex = r'var def = (.*);'
    re_result = re.search(regex, http_result.text)
    if re_result is None:
        return "缺少模版数据"
    def_string = re_result.group(1)
    def_data = json.loads(def_string)
    api_string = def_data["geo_api_info"].replace(r'\"', '"')
    if len(api_string.strip()) == 0:
        return "缺少定位数据"
    api_data = json.loads(api_string)
    sign_data["geo_api_info"] = str(api_string)
    sign_data["address"] = api_data["formattedAddress"]
    sign_data["area"] = api_data["addressComponent"]["province"] \
                        + api_data["addressComponent"]["city"] \
                        + api_data["addressComponent"]["district"]
    sign_data["province"] = api_data["addressComponent"]["province"]
    sign_data["city"] = api_data["addressComponent"]["city"]
    if sign_data["province"] in ('长沙市', '上海市', '重庆市', '天津市'):
        sign_data["city"] = sign_data["province"]

    # 重发数据完成签到
    url = "https://wxxy.csu.edu.cn/ncov/wap/default/save"
    try:
        http_result = session.post(url, data=sign_data)
    except requests.exceptions.ReadTimeout:
        print("requests.exceptions.ReadTimeout:[%s]" % url)
        return "自动签到失败"
    except requests.exceptions.ConnectionError:
        print("requests.exceptions.ConnectionError:[%s]" % url)
        return "自动签到失败"
    return json.loads(http_result.text)


def unix_time(unit=1):
    return int(time.time() * unit)


def str_time(pattern='%Y-%m-%d %H:%M:%S'):
    return time.strftime(pattern, time.localtime(time.time()))


if __name__ == "__main__":
    main()

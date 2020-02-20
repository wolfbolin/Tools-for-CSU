# coding=utf-8、
import time
import json
import requests
from my_config import cookies
from my_config import sign_data


def main():
    sign_time = 1025   # 表示 上午十点二十五分 开始发起签到
    time_now = int(str_time("%H%M"))
    while time_now < sign_time:
        print("未到指定的签到时间")
        time.sleep(5)
        time_now = int(str_time("%H%M"))

    while True:
        sign_res = sign_in()
        if sign_res != "":
            sign_res = json.loads(sign_res)
            if sign_res["e"] == 0:
                print("今日签到提交成功，msg:", sign_res)
            elif sign_res["e"] == 1 and sign_res["m"] == "今天已经填报了":
                print("今天已完成签到，msg:", sign_res)
                break
            else:
                print("未知的错误，msg:", sign_res)

        time.sleep(5)

    print("程序退出")


def sign_in():
    url = "https://wxxy.csu.edu.cn/ncov/wap/default/save"
    try:
        headers = {
            "User-Agent": "Python scripts by wolfbolin",
            "Cookie": cookies
        }
        sign_data["id"] = int(sign_data["id"])
        sign_data["date"] = str_time("%Y%m%d")
        sign_data["created"] = unix_time()

        http_result = requests.post(url, data=sign_data, headers=headers, timeout=(2, 30))
        return http_result.text
    except requests.exceptions.ReadTimeout:
        print("requests.exceptions.ReadTimeout:[%s]" % url)
        return ""
    except requests.exceptions.ConnectionError:
        print("requests.exceptions.ConnectionError:[%s]" % url)
        return ""


def unix_time(unit=1):
    return int(time.time() * unit)


def str_time(pattern='%Y-%m-%d %H:%M:%S'):
    return time.strftime(pattern, time.localtime(time.time()))


if __name__ == "__main__":
    main()

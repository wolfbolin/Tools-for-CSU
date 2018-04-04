from urllib import parse
import hashlib
import requests

header_info = {
    'Host': 'mooc1-2.chaoxing.com',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

print("Thanks for using AutoPlayer v0.1 by wolfbolin\n")
print("I am ready to complete it.")

cookie = input("Please enter the cookies")

while True:
    url = input("Please enter the URL")
    url_info = parse.urlparse(url)
    url_params = parse.parse_qs(url_info.query, True)

    enc = ""
    enc += "[" + url_params['clazzId'][0] + "]"
    enc += "[" + url_params['userid'][0] + "]"
    enc += "[" + url_params['jobid'][0] + "]"
    enc += "[" + url_params['objectId'][0] + "]"
    # enc += "[" + str(int(url_params['playingTime'][0]) * 1000) + "]"
    enc += "[" + str(int(url_params['duration'][0]) * 1000) + "]"
    enc += "[d_yHJ!$pdA~5]"
    enc += "[" + str(int(url_params['duration'][0]) * 1000) + "]"
    enc += "[" + url_params['clipTime'][0] + "]"
    enc = hashlib.md5(enc.encode('utf-8')).hexdigest()

    data = {}
    for key in url_params:
        data[key] = url_params[key][0]
    data['playingTime'] = data['duration']
    data['isdrag'] = '4'
    data['enc'] = enc

    cookies = {}
    for line in cookie.split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value

    url = "http://" + url_info.netloc + url_info.path + "?" + parse.urlencode(data)

    print(url)
    print(data)
    print(cookies)

    res = requests.get(url, headers=header_info, cookies=cookies)
    print(res.content)
    print("\nYou watched this video just now.\nThanks for using AutoPlayer v0.1 by wolfbolin\n\n- - - END - - -")

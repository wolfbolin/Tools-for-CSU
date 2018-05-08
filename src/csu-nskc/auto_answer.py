import requests
import json

header_info = {
    'Host': 'yiban.csu.edu.cn',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://yiban.csu.edu.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'http://yiban.csu.edu.cn/csuNSKC/',
    'Content-Type': 'application/json'
}
start_test_url = "http://yiban.csu.edu.cn/csuNSKC/test/startTest"
submit_test_url = "http://yiban.csu.edu.cn/csuNSKC/test/submitTest"


if __name__ == '__main__':
    print("Thanks for using Auto_answer v0.1 by wolfbolin\n")
    print("I am ready to complete it.")
    cookie = input("请填入Cookies信息")
    cookies = {}
    student_info = 0
    for line in cookie.split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
        if name == 'signon':
            student_info = json.loads(value)
    test_id = input("请选择自动测试答题或自动初试考试(0 or 1)")
    test_record = {
        'studentId': student_info['studentId'],
        'testId': test_id
    }

    res = requests.post(start_test_url, headers=header_info, cookies=cookies, data=json.dumps(test_record))
    title_data = json.loads(res.content)
    title_data.pop('judgeList')
    title_data.pop('caseList')
    title_data.pop('discussList')
    title_data['caseAnswer'] = None
    title_data['discussAnswer'] = None

    ans_data = {
        'submitPaper': title_data,
        'testrecord': test_record
    }

    res = requests.post(submit_test_url, headers=header_info, cookies=cookies, data=json.dumps(ans_data))
    print(json.loads(res.content))

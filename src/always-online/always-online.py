import time
import subprocess

import schedule
from selenium import webdriver

import credentials

lyric_generator = None


def get_lyric():
    lyrics = []
    n = 0
    with open('lyrics.txt') as f:
        for line in f:
            lyrics.append(line[0:len(line) - 1])
    while True:
        yield lyrics[n % len(lyrics)]
        n += 1


def check_and_login():
    # Show lyric
    global lyric_generator
    if lyric_generator is None:
        lyric_generator = get_lyric()
    print(next(lyric_generator))

    # Watch website for 3 times
    failed_count = 0
    for i in range(1, 4):
        if subprocess.call('ping www.qq.com -c 1 -t 2', shell=True, stdout=subprocess.DEVNULL):
            failed_count += 1

    # 3 times all failed
    if failed_count >= 3:
        print('\n哎呀...掉线了！尝试恢复...', end='')
        driver = webdriver.Chrome()
        driver.get('http://172.16.0.101/')
        time.sleep(3)
        driver.find_element_by_id('username').send_keys(credentials.username)
        driver.find_element_by_id("pwd_tip").click()
        driver.find_element_by_id("pwd").send_keys(credentials.password)
        driver.find_element_by_id("loginLink").click()
        print('应该已经恢复啦！')
    print('\n')


check_and_login()

schedule.every(30).seconds.do(check_and_login)

while True:
    schedule.run_pending()
    time.sleep(1)

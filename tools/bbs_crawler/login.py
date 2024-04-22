import argparse
import time
from common import get_rand_int
import requests


def _login(session, user_name, pwd):
    url = "https://bbs.byr.cn/user/ajax_login.json"
    payload = "id={}&passwd={}&mode=0&CookieDate=0".format(user_name, pwd)
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://bbs.byr.cn',
        'pragma': 'no-cache',
        'referer': 'https://bbs.byr.cn/index',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    response = session.post(url, headers=headers, data=payload)
    print(response.text)


def _logout(session):
    url = "https://bbs.byr.cn/user/ajax_logout.json"
    payload = {}
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://bbs.byr.cn/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    resp = session.get(url, headers=headers, data=payload)
    print("-"*100)
    print(resp.text)
    print("-"*100)
    print(resp.headers)
    print("-"*100)
    print(session.cookies)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="脚本描述信息")
    # 添加参数
    parser.add_argument("-u", "--user_name", help="用户名", type=str, default='hzplszl')
    parser.add_argument("-p", "--pwd", help="pwd", type=str, default='lslhcqy')
    params = parser.parse_args()
    print(params.user_name, params.pwd)
    time.sleep(get_rand_int(1, 60))
    s = requests.session()
    _login(s, params.user_name, params.pwd)
    time.sleep(get_rand_int(30, 60))
    _logout(s)
    time.sleep(get_rand_int(12, 60))

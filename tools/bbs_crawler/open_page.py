import time
import argparse
from common import get_rand_int
import requests
from tools.bbs_crawler.login import _login, _logout



def my_favor(session, user_name):
    url = "https://bbs.byr.cn/favor/ajax_list.json?uid={}&root=list-favor".format(user_name)
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
    response = session.get(url, headers=headers, data=payload)
    print("-"*100)
    print(response.text)
    print("-"*100)
    print(response.headers)
    print("-"*100)
    print(session.cookies)


def open_board(session, user_name, board_name):
    url = "https://bbs.byr.cn/board/{}?_uid={}".format(board_name, user_name)
    payload = {}
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': '*/*',
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
    response = session.get(url, headers=headers, data=payload)
    print("-"*100)
    print(response.text)
    print("-"*100)
    print(response.headers)
    print("-"*100)
    print(session.cookies)




def open_anxianlianghua_page(session, user_name):
    url = "https://bbs.byr.cn/article/ParttimeJob/919307?_uid={}".format(user_name)

    payload = {}
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': '*/*',
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
    response = session.get(url, headers=headers, data=payload)
    print("-"*100)
    print(response.text)
    print("-"*100)
    print(response.headers)
    print("-"*100)
    print(session.cookies)


def anxianlianghua_reply(session):
    url = "https://bbs.byr.cn/article/ParttimeJob/ajax_post.json"

    payload = "content=a%0A&id=919307&subject=Re%253A%2520%25E3%2580%2590%25E5%2586%2585%25E6%258E%25A8%25E3%2580%2591%25E3%2580%2590%25E5%25AE%2589%25E8%25B4%25A4%25E9%2587%258F%25E5%258C%2596%25E3%2580%2591%25E9%2587%258F%25E5%258C%2596%252F%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE%252F%25E8%25BF%2590%25E7%25BB%25B4%25E7%25A0%2594%25E5%258F%2591"
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://bbs.byr.cn',
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

    response = session.post(url, headers=headers, data=payload)
    print("-"*100)
    print(response.text)
    print("-"*100)
    print(response.headers)
    print("-"*100)
    print(session.cookies)


def open_weiguanboyi_page(session, user_name):
    url = "https://bbs.byr.cn/article/ParttimeJob/918956?_uid={}".format(user_name)
    payload = {}
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': '*/*',
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
    response = session.get(url, headers=headers, data=payload)
    print("-"*100)
    print(response.text)
    print("-"*100)
    print(response.headers)
    print("-"*100)
    print(session.cookies)


def weiguanboyi_reply(session):
    url = "https://bbs.byr.cn/article/ParttimeJob/ajax_post.json"
    payload = "content=a&id=918956&subject=Re%253A%2520%25E3%2580%2590%25E5%2586%2585%25E6%258E%25A8%25E3%2580%2591%25E3%2580%2590%25E5%25BE%25AE%25E8%25A7%2582%25E5%258D%259A%25E6%2598%2593%25E3%2580%2591%25E9%2587%258F%25E5%258C%2596%25E7%25A0%2594%25E5%258F%2591%252F%25E7%25A0%2594%25E7%25A9%25B6%25E5%2591%2598%252F%25E5%25AE%259E%25E4%25B9%25A0%252FHR"
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://bbs.byr.cn',
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
    response = session.post(url, headers=headers, data=payload)
    print("-"*100)
    print(response.text)
    print("-"*100)
    print(response.headers)
    print("-"*100)
    print(session.cookies)


def open_bytedance_page(session, user_name):
    url = "https://bbs.byr.cn/article/ParttimeJob/918954?_uid={}".format(user_name)
    payload = {}
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': '*/*',
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
    response = session.get(url, headers=headers, data=payload)
    print("-"*100)
    print(response.text)
    print("-"*100)
    print(response.headers)
    print("-"*100)
    print(session.cookies)


def bytedance_reply(session):
    url = "https://bbs.byr.cn/article/ParttimeJob/ajax_post.json"
    payload = "content=a&id=918954&subject=Re%253A%2520%25E3%2580%2590%25E5%2586%2585%25E6%258E%25A8%25E3%2580%2591%25E3%2580%2590%25E5%25AD%2597%25E8%258A%2582%25E3%2580%2591%25E7%2594%25B5%25E5%2595%2586%25E6%2596%25B9%25E5%2590%2591%25E7%25A0%2594%25E5%258F%2591%252F%25E7%25AE%2597%25E6%25B3%2595%252F%25E8%25BF%2590%25E8%2590%25A5%252F%25E4%25BA%25A7%25E5%2593%2581"
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://bbs.byr.cn',
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
    response = session.post(url, headers=headers, data=payload)
    print("-"*100)
    print(response.text)
    print("-"*100)
    print(response.headers)
    print("-"*100)
    print(session.cookies)

def open_page(session, board_name, post_id, user_name):
    url = "https://bbs.byr.cn/article/{}/{}?_uid={}".format(board_name, post_id, user_name)
    payload = {}
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': '*/*',
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
    response = session.get(url, headers=headers, data=payload)
    print("-"*100)
    print(response.text)
    print("-"*100)
    print(response.headers)
    print("-"*100)
    print(session.cookies)



def open_ms_page(session, user_name):
    url = "https://bbs.byr.cn/article/ParttimeJob/918955?_uid={}".format(user_name)
    payload = {}
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': '*/*',
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
    response = session.get(url, headers=headers, data=payload)
    print("-"*100)
    print(response.text)
    print("-"*100)
    print(response.headers)
    print("-"*100)
    print(session.cookies)


def ms_reply(session):
    import requests
    url = "https://bbs.byr.cn/article/ParttimeJob/ajax_post.json"
    payload = "content=1&id=918955&subject=Re%253A%2520%25E3%2580%2590%25E5%2586%2585%25E6%258E%25A8%25E3%2580%2591%25E3%2580%2590%25E5%25BE%25AE%25E8%25BD%25AF%25E3%2580%2591%25E7%25AE%2597%25E6%25B3%2595%252F%25E7%25A0%2594%25E5%258F%2591%252F%25E4%25BA%25A7%25E5%2593%2581%252F%25E7%25A0%2594%25E7%25A9%25B6%25E5%2591%2598"
    headers = {
        'authority': 'bbs.byr.cn',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://bbs.byr.cn',
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
    response = session.post(url, headers=headers, data=payload)
    print("-"*100)
    print(response.text)
    print("-"*100)
    print(response.headers)
    print("-"*100)
    print(session.cookies)


def auto_open_page(user_name, pwd, board_name, page_id):
    time.sleep(get_rand_int(1, 60))
    s = requests.session()
    _login(s, user_name, pwd)
    time.sleep(get_rand_int(12, 60))
    my_favor(s, user_name)
    time.sleep(get_rand_int(8, 60))
    s.cookies.set("nforum-left", "010", domain=".bbs.byr.cn", path="/")
    open_board(s, user_name, board_name)
    time.sleep(get_rand_int(5, 60))
    open_anxianlianghua_page(s, user_name)
    time.sleep(get_rand_int(5, 60))
    anxianlianghua_reply(s)
    time.sleep(get_rand_int(35, 60))
    open_weiguanboyi_page(s, user_name)
    time.sleep(get_rand_int(5, 60))
    weiguanboyi_reply(s)
    time.sleep(get_rand_int(38, 60))
    open_bytedance_page(s, user_name)
    time.sleep(get_rand_int(5, 60))
    bytedance_reply(s)
    time.sleep(get_rand_int(38, 60))
    open_ms_page(s, user_name)
    time.sleep(get_rand_int(5, 60))
    ms_reply(s)
    time.sleep(get_rand_int(30, 60))
    _logout(s)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="脚本描述信息")
    # 添加参数
    parser.add_argument("-u", "--user_name", help="用户名", type=str, default='hzplszl')
    parser.add_argument("-p", "--pwd", help="pwd", type=str, default='lslhcqy')
    parser.add_argument("-b", "--board", help="board_name", type=str, default='ParttimeJob')
    parser.add_argument("-t", "--tiezi", help="帖子id", type=int, default=918955)
    params = parser.parse_args()
    time.sleep(get_rand_int(1, 60))
    s = requests.session()
    _login(s, params.user_name, params.pwd)
    time.sleep(get_rand_int(12, 60))
    my_favor(s, params.user_name)
    time.sleep(get_rand_int(8, 60))
    s.cookies.set("nforum-left", "010", domain=".bbs.byr.cn", path="/")
    open_board(s, params.user_name, params.board)
    time.sleep(get_rand_int(5, 60))
    open_page(s, params.board, params.tiezi, params.user_name)
    time.sleep(get_rand_int(40, 80))
    _logout(s)


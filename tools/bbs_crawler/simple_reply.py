import time
import argparse
from common import get_rand_int
import requests
from tools.bbs_crawler.login import _login, _logout
from tools.bbs_crawler.open_page import open_board, open_page, my_favor
import urllib.parse

def simple_up_page_reply(session, board_name, post_id, title = 'Re', content='a'):
    params = {'content': content, 'id': post_id, 'subject': urllib.parse.quote(title)}
    url = "https://bbs.byr.cn/article/{}/ajax_post.json".format(board_name)
    payload = urllib.parse.urlencode(params)
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
    time.sleep(get_rand_int(10, 40))
    simple_up_page_reply(s, params.board, params.tiezi)
    time.sleep(get_rand_int(40, 80))
    _logout(s)


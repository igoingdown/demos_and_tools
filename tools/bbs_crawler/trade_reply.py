import time
import argparse
from common import get_rand_int
import requests
from tools.bbs_crawler.login import _login, _logout
from tools.bbs_crawler.open_page import open_board, open_page, my_favor
from tools.bbs_crawler.simple_reply import simple_up_page_reply



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="脚本描述信息")
    # 添加参数
    parser.add_argument("-u", "--user_name", help="用户名", type=str, default='hzplszl')
    parser.add_argument("-p", "--pwd", help="pwd", type=str, default='lslhcqy')
    parser.add_argument("-b", "--board", help="board_name", type=str, default='Advertising')
    parser.add_argument("-t", "--tiezi", help="帖子id", type=int, default=2087585)
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
    time.sleep(get_rand_int(60, 1200))

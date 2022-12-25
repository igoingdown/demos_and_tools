import requests
import json
import time
from common import get_rand_int
import datetime
from post import post_bytedance_lightning_referral


def __crawl_top_ten():
    url = "https://bbs.byr.cn/n/b/board/JobInfo.json?page=1"
    payload = {}
    headers = {
        'authority': 'bbs.byr.cn',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'x-requested-with': 'XMLHttpRequest',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://bbs.byr.cn/n/board/JobInfo',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'nforum-left=010; Hm_lvt_38b0e830a659ea9a05888b924f641842=1613630796,1613813567; nforum[BMODE]=2; nforum[XWJOKE]=hoho; login-user=xsz; nforum[UTMPUSERID]=xsz; nforum[PASSWORD]=5uul4D8KRqDE2wkoO5Jw1A%3D%3D; nforum[UTMPKEY]=84965111; nforum[UTMPNUM]=4870; Hm_lpvt_38b0e830a659ea9a05888b924f641842=1613986270; nforum[site]=yamb'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        m = json.loads(response.text.encode('utf8'))
        return m["data"]["posts"][:10]
    except:
        print(response)
        return []


def __find_xsz(posts):
    if posts is None or len(posts) == 0:
        return False
    for post in posts:
        if post['poster'] == 'xsz' or post['poster'] == 'fycjmingxing':
            return True
    return False


def infinite_monitor():
    while True:
        if get_part_of_day() != "night":
            time.sleep(get_rand_int(100, 1000))
            continue
        top10_posts = __crawl_top_ten()
        if __find_xsz(top10_posts):
            print(datetime.datetime.now(), "ok")
        else:
            print(datetime.datetime.now(), "FBI WARNING: not found")
            '''
            time.sleep(get_rand_int(20, 50))
            post_bytedance_lightning_referral()
            '''
        time.sleep(get_rand_int(100, 1000))


def get_part_of_day():
    h = datetime.datetime.now().hour
    return (
        "morning"
        if 5 <= h <= 11
        else "afternoon"
        if 12 <= h <= 21
        else "evening"
        if 22 <= h <= 23
        else "night"
    )


# To use current hour:
# from datetime import datetime
# part =
# print(f"Have a good {part}!")

if __name__ == '__main__':
    infinite_monitor()


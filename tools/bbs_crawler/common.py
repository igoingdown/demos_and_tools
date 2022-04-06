import random


def get_rand_int(a, b):
    random.seed()
    return random.randint(a, b)


def read_post_common_header_and_params():
    headers = {
        'authority': 'bbs.byr.cn',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://bbs.byr.cn/',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'login-user=fycjmingxing; nforum-left=010; Hm_lvt_38b0e830a659ea9a05888b924f641842=1646320015,1646369866,1646393455,1646565081; nforum[UTMPUSERID]=fycjmingxing; nforum[PASSWORD]=EfB0Gy0o6IeuhB5MLcOD0Q%3D%3D; Hm_lpvt_38b0e830a659ea9a05888b924f641842=1646565083; nforum[BMODE]=2; nforum[XWJOKE]=hoho; nforum[UTMPKEY]=98618392; nforum[UTMPNUM]=7197',
    }

    params = (
        ('_uid', 'fycjmingxing'),
    )
    return headers, params


def add_comment_header():
    headers = {
        'authority': 'bbs.byr.cn',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://bbs.byr.cn',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://bbs.byr.cn/',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'login-user=fycjmingxing; nforum-left=010; Hm_lvt_38b0e830a659ea9a05888b924f641842=1646320015,1646369866,1646393455,1646565081; nforum[UTMPUSERID]=fycjmingxing; nforum[PASSWORD]=EfB0Gy0o6IeuhB5MLcOD0Q%3D%3D; Hm_lpvt_38b0e830a659ea9a05888b924f641842=1646565083; nforum[BMODE]=2; nforum[XWJOKE]=hoho; nforum[UTMPKEY]=98618392; nforum[UTMPNUM]=7197',
    }
    return headers

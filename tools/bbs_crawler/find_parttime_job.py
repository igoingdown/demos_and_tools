import requests


def _find_parttime_job():
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
        'cookie': 'login-user=fycjmingxing; nforum-left=010; Hm_lvt_38b0e830a659ea9a05888b924f641842=1646233095,1646312906,1646320015,1646369866; nforum[UTMPUSERID]=fycjmingxing; nforum[UTMPKEY]=47529434; nforum[UTMPNUM]=7109; nforum[PASSWORD]=EfB0Gy0o6IeuhB5MLcOD0Q%3D%3D; nforum[BMODE]=2; nforum[XWJOKE]=hoho; Hm_lpvt_38b0e830a659ea9a05888b924f641842=1646371311',
        'if-modified-since': 'Thu, 03 Mar 2022 15:27:06 GMT',
    }

    params = (
        ('_uid', 'fycjmingxing'),
    )

    response = requests.get('https://bbs.byr.cn/board/ParttimeJob', headers=headers, params=params)
    print(response.status_code, response.content)


if __name__ == '__main__':
    _find_parttime_job()



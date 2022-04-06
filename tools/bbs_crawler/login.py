import requests


def _login():
    headers = {
        'authority': 'bbs.byr.cn',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'login-user=fycjmingxing; nforum-left=010; Hm_lvt_38b0e830a659ea9a05888b924f641842=1646233095,1646312906,1646320015,1646369866; nforum[UTMPUSERID]=fycjmingxing; nforum[UTMPKEY]=47529434; nforum[UTMPNUM]=7109; nforum[PASSWORD]=EfB0Gy0o6IeuhB5MLcOD0Q%3D%3D; nforum[BMODE]=2; nforum[XWJOKE]=hoho; Hm_lpvt_38b0e830a659ea9a05888b924f641842=1646370465',
    }

    response = requests.get('https://bbs.byr.cn/', headers=headers)

    print(response.text, response.status_code, response.content)


if __name__ == '__main__':
    _login()

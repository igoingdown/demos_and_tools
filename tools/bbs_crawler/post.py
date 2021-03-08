import requests
import time
from common import get_rand_int


def _new_article():
    url = "https://bbs.byr.cn/article/JobInfo/post?_uid=xsz"
    payload = {}
    headers = {
        'authority': 'bbs.byr.cn',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://bbs.byr.cn/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'nforum-left=010; Hm_lvt_38b0e830a659ea9a05888b924f641842=1613630796,1613813567; nforum[BMODE]=2; nforum[XWJOKE]=hoho; login-user=xsz; nforum[UTMPUSERID]=xsz; nforum[PASSWORD]=5uul4D8KRqDE2wkoO5Jw1A%3D%3D; nforum[site]=yamb; nforum[UTMPKEY]=7805872; nforum[UTMPNUM]=3934; Hm_lpvt_38b0e830a659ea9a05888b924f641842=1614151728; nforum[UTMPKEY]=84124474; nforum[UTMPNUM]=4291; nforum[XWJOKE]=hoho'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        print(response.text)
        return 0
    except Exception as e:
        print(e)
        return -1


def _submit_article():
    url = "https://bbs.byr.cn/article/JobInfo/ajax_post.json"
    payload = "subject=%E3%80%90%E5%86%85%E6%8E%A8%E3%80%91%E3%80%90%E5%AE%9E%E4%B9%A0%E3%80%91%E3%80%90%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8%E3%80%91%E9%97%AA%E7%94%B5%E5%86%85%E6%8E%A8&content=----------------------------------------------------%0A%0A%5Bb%5D%E5%A4%9A%E6%AC%A1%E6%8A%95%E9%80%92%E4%B8%8D%E8%83%BD%E5%A2%9E%E5%8A%A0%E5%85%A5%E8%81%8C%E6%9C%BA%E4%BC%9A%EF%BC%81%E6%89%AB%E7%A0%81%E6%8A%95%E9%80%92%E4%B9%8B%E5%89%8D%E5%85%88%E8%81%94%E7%B3%BB%E4%B8%80%E4%B8%8B%EF%BC%8C%E5%B8%AE%E6%94%B9%E7%AE%80%E5%8E%86%EF%BC%81%0A%E5%A4%9A%E6%AC%A1%E6%8A%95%E9%80%92%E4%B8%8D%E8%83%BD%E5%A2%9E%E5%8A%A0%E5%85%A5%E8%81%8C%E6%9C%BA%E4%BC%9A%EF%BC%81%E6%89%AB%E7%A0%81%E6%8A%95%E9%80%92%E4%B9%8B%E5%89%8D%E5%85%88%E8%81%94%E7%B3%BB%E4%B8%80%E4%B8%8B%EF%BC%8C%E5%B8%AE%E6%94%B9%E7%AE%80%E5%8E%86%EF%BC%81%0A%E5%A4%9A%E6%AC%A1%E6%8A%95%E9%80%92%E4%B8%8D%E8%83%BD%E5%A2%9E%E5%8A%A0%E5%85%A5%E8%81%8C%E6%9C%BA%E4%BC%9A%EF%BC%81%E6%89%AB%E7%A0%81%E6%8A%95%E9%80%92%E4%B9%8B%E5%89%8D%E5%85%88%E8%81%94%E7%B3%BB%E4%B8%80%E4%B8%8B%EF%BC%8C%E5%B8%AE%E6%94%B9%E7%AE%80%E5%8E%86%EF%BC%81%5B%2Fb%5D%0A%0A----------------------------------------------------%0A%0A%5Bema0%5D%5Bema0%5D%5Bema0%5D%5Bema0%5D%5Bema0%5D%5Bema0%5D%5Bema0%5D%5Bema0%5D%5Bema0%5D%0A%0A----------------------------------------------------%0A%0A%E6%9C%AC%E6%AC%A1%E5%86%85%E6%8E%A8%E4%BB%85%E9%92%88%E5%AF%B9%E6%8A%80%E6%9C%AF%E7%A0%94%E5%8F%91%E7%B1%BB%E5%B2%97%E4%BD%8D%0A%E3%80%90%E5%86%85%E6%8E%A8%E6%97%B6%E9%97%B4%E3%80%91%5Bb%5D2021%2F1%2F28-2021%2F7%2F31%5B%2Fb%5D%0A%E3%80%90%E6%8B%9B%E8%81%98%E5%AF%B9%E8%B1%A1%E3%80%91%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86%E7%9A%84%E6%89%80%E6%9C%89%E5%9C%A8%E6%A0%A1%E7%94%9F%0A%E3%80%90%E6%8A%95%E9%80%92%E9%93%BE%E6%8E%A5%E3%80%91%5Bb%5Dhttps%3A%2F%2Fjob.toutiao.com%2Fs%2Fe1X5ypS%5B%2Fb%5D%0A%E3%80%90%E5%B7%A5%E4%BD%9C%E5%9C%B0%E7%82%B9%E3%80%91%E5%8C%97%E4%BA%AC%E3%80%81%E4%B8%8A%E6%B5%B7%E3%80%81%E6%B7%B1%E5%9C%B3%E3%80%81%E6%AD%A6%E6%B1%89%E3%80%81%E6%9D%AD%E5%B7%9E%E3%80%81%E6%88%90%E9%83%BD%E3%80%81%E5%8D%97%E4%BA%AC%E3%80%81%E5%B9%BF%E5%B7%9E%E3%80%81%E5%8E%A6%E9%97%A8%0A%0A----------------------------------------------------%0A%0A%E5%AE%9E%E4%B9%A0%E8%96%AA%E8%B5%84%EF%BC%9A400%EF%BC%8F%E5%A4%A9%0A%E5%85%8D%E8%B4%B9%E4%B8%89%E9%A4%90%EF%BC%8C%E5%B0%B1%E8%BF%91%E7%A7%9F%E6%88%BF%E8%A1%A5%E8%B4%B41500%0A%0A----------------------------------------------------%0A%0A%E8%81%94%E7%B3%BB%E6%96%B9%E5%BC%8F(%E5%BE%AE%E4%BF%A1%26%E7%94%B5%E8%AF%9D)%EF%BC%9A%5Bb%5D18810860130%5B%2Fb%5D%0A%E8%81%94%E7%B3%BB%E6%96%B9%E5%BC%8F(%E5%BE%AE%E4%BF%A1%26%E7%94%B5%E8%AF%9D)%EF%BC%9A%5Bb%5D18810860130%5B%2Fb%5D%0A%E8%81%94%E7%B3%BB%E6%96%B9%E5%BC%8F(%E5%BE%AE%E4%BF%A1%26%E7%94%B5%E8%AF%9D)%EF%BC%9A%5Bb%5D18810860130%5B%2Fb%5D%0A%0A----------------------------------------------------%0A%0A%E3%80%90%E6%88%91%E4%BB%AC%E7%9A%84%E5%85%AC%E5%8F%B8%E3%80%91%0A%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8%E6%88%90%E7%AB%8B%E4%BA%8E2012%E5%B9%B43%E6%9C%88%EF%BC%8C%E5%85%AC%E5%8F%B8%E4%BD%BF%E5%91%BD%E4%B8%BA%E2%80%9CInspire+Creativity%2C+Enrich+Life%EF%BC%88%E6%BF%80%E5%8F%91%E5%88%9B%E9%80%A0%EF%BC%8C%E4%B8%B0%E5%AF%8C%E7%94%9F%E6%B4%BB%EF%BC%89%E2%80%9D%E3%80%82%E5%85%AC%E5%8F%B8%E4%B8%9A%E5%8A%A1%E8%A6%86%E7%9B%96150%E4%B8%AA%E5%9B%BD%E5%AE%B6%E5%92%8C%E5%9C%B0%E5%8C%BA%E3%80%8175%E4%B8%AA%E8%AF%AD%E7%A7%8D%EF%BC%8C%E6%8B%A5%E6%9C%89%E8%B6%85%E8%BF%876%E4%B8%87%E5%90%8D%E5%91%98%E5%B7%A5%E3%80%82%0A%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8%E5%9C%A8%E5%85%A8%E7%90%83%E6%8E%A8%E5%87%BA%E4%BA%86%E5%A4%9A%E6%AC%BE%E6%9C%89%E5%BD%B1%E5%93%8D%E5%8A%9B%E7%9A%84%E4%BA%A7%E5%93%81%EF%BC%8C%E5%8C%85%E6%8B%AC%E4%BB%8A%E6%97%A5%E5%A4%B4%E6%9D%A1%E3%80%81%E6%8A%96%E9%9F%B3%E3%80%81%E8%A5%BF%E7%93%9C%E8%A7%86%E9%A2%91%E3%80%81%E9%A3%9E%E4%B9%A6%E3%80%81TikTok%E3%80%81Lark%E3%80%81Helo%E7%AD%89%E3%80%82%E6%88%AA%E8%87%B32020%E5%B9%B41%E6%9C%88%EF%BC%8C%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8%E6%97%97%E4%B8%8B%E4%BA%A7%E5%93%81%E5%85%A8%E7%90%83%E6%9C%88%E6%B4%BB%E8%B7%83%E7%94%A8%E6%88%B7%E6%95%B0%E8%B6%85%E8%BF%8715%E4%BA%BF%E3%80%82%0A%0A----------------------------------------------------%0A%0A%E3%80%90%E6%88%91%E4%BB%AC%E7%9A%84%E4%BC%98%E5%8A%BF%E3%80%91%0A-+%E8%87%AA%E7%94%B1%E5%B9%B3%E7%AD%89%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%8E%AF%E5%A2%83%0A++-+%E7%81%B5%E6%B4%BB%E7%9A%84%E5%8A%9E%E5%85%AC%E6%97%B6%E9%97%B4%EF%BC%8C%E4%B8%8A%E7%8F%AD%E4%B8%8D%E6%89%93%E5%8D%A1%0A++-+%E5%B9%B3%E7%AD%89%E7%9A%84%E5%B7%A5%E4%BD%9C%E6%B0%9B%E5%9B%B4%EF%BC%8C%E6%B2%9F%E9%80%9A%E6%97%A0%E2%80%9C%E5%A4%A7%E5%B0%8F%E2%80%9D%0A-+%E5%85%B3%E6%B3%A8%E6%AF%8F%E4%B8%80%E4%BD%8D%E6%A0%A1%E6%8B%9B%E6%96%B0%E4%BA%BA%E7%9A%84%E6%88%90%E9%95%BF%0A++-+Mentor%E5%88%B6%EF%BC%8C%E5%88%9D%E5%85%A5%E8%81%8C%E5%9C%BA%E4%BD%A0%E6%9C%89%E4%B8%80%E4%BD%8D%E2%80%9C%E9%A2%86%E8%B7%AF%E4%BA%BA%E2%80%9D%0A++-+Dance%E8%88%9E%E8%AE%A1%E5%88%92%EF%BC%8C%E5%BA%94%E5%B1%8A%E7%94%9F%E4%B8%93%E5%B1%9E%E5%9F%B9%E5%85%BB%E8%AE%A1%E5%88%92%0A++-+Bootcamp%EF%BC%8C%E6%8A%80%E6%9C%AF%E6%96%B0%E4%BA%BA%E8%AE%AD%E7%BB%83%E8%90%A5%0A++-+ByteTalk%EF%BC%8C%E8%A1%8C%E4%B8%9A%E5%89%8D%E6%B2%BF%E8%B5%84%E8%AE%AF%E5%88%86%E4%BA%AB%0A-+%E5%85%A8%E6%96%B9%E4%BD%8D%E7%9A%84%E8%B4%B4%E5%BF%83%E7%A6%8F%E5%88%A9%E5%85%B3%E6%80%80%0A++-+%E5%85%8D%E8%B4%B9%E4%B8%89%E9%A4%90%E5%92%8C%E5%B0%B1%E8%BF%91%E4%BD%8F%E6%88%BF%E8%A1%A5%E8%B4%B4%EF%BC%8C%E5%B8%AE%E4%BD%A0%E5%87%8F%E8%BD%BB%E5%8E%8B%E5%8A%9B%0A++-+%E5%AE%8C%E5%96%84%E7%9A%84%E5%95%86%E4%B8%9A%E4%BF%9D%E9%99%A9%E5%88%B6%E5%BA%A6%EF%BC%8C%E5%AE%88%E6%8A%A4%E4%BD%A0%E7%9A%84%E5%89%8D%E8%A1%8C%0A++-+%E6%B8%A9%E6%9A%96%E7%9A%84%E8%8A%82%E6%97%A5%E7%A4%BC%E5%93%81%EF%BC%8C%E7%82%B9%E4%BA%AE%E6%AF%8F%E4%B8%80%E4%B8%AA%E5%80%BC%E5%BE%97%E5%BA%86%E7%A5%9D%E7%9A%84%E6%97%A5%E5%AD%90%0A++-+%E5%A4%9A%E6%A0%B7%E5%8C%96%E7%9A%84%E5%81%A5%E5%BA%B7%E5%85%B3%E6%80%80%EF%BC%8C%E5%8A%A9%E4%BD%A0%E6%9B%B4%E5%A5%BD%E5%9C%B0%E5%B7%A5%E4%BD%9C%E7%94%9F%E6%B4%BB%0A-+%E7%B2%BE%E5%BD%A9%E5%A4%9A%E5%85%83%E7%9A%84%E6%96%87%E5%8C%96%E7%94%9F%E6%B4%BB%0A++-+%E5%AE%9A%E6%9C%9F%E4%B8%BE%E5%8A%9ECEO%E9%9D%A2%E5%AF%B9%E9%9D%A2%0A++-+%E6%AC%A2%E4%B9%90%E6%B8%A9%E9%A6%A8%E7%9A%84%E5%AE%B6%E5%BA%AD%E5%BC%80%E6%94%BE%E6%97%A5%0A++-+%E5%8A%A0%E5%85%A5%E5%85%B4%E8%B6%A3%E7%A4%BE%E5%9B%A2%EF%BC%8C%E5%AF%BB%E6%89%BE%E5%BF%97%E8%B6%A3%E7%9B%B8%E6%8A%95%E7%9A%84%E6%9C%8B%E5%8F%8B%0A%0A----------------------------------------------------%0A&signature=0&id=0"
    headers = {
        'authority': 'bbs.byr.cn',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://bbs.byr.cn',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://bbs.byr.cn/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'nforum-left=010; Hm_lvt_38b0e830a659ea9a05888b924f641842=1613630796,1613813567; nforum[BMODE]=2; nforum[XWJOKE]=hoho; login-user=xsz; nforum[UTMPUSERID]=xsz; nforum[PASSWORD]=5uul4D8KRqDE2wkoO5Jw1A%3D%3D; nforum[site]=yamb; Hm_lpvt_38b0e830a659ea9a05888b924f641842=1614151728; nforum[UTMPKEY]=54866187; nforum[UTMPNUM]=4172; nforum[UTMPKEY]=84124474; nforum[UTMPNUM]=4291; nforum[XWJOKE]=hoho'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        print(response.text)
        return 0
    except Exception as e:
        print(e)
        return 1


def post_bytedance_lightning_referral():
    if _new_article() != 0:

        return 1
    time.sleep(get_rand_int(10, 60))
    if _submit_article() != 0:
        return 2
    return 0


if __name__ == '__main__':
    if post_bytedance_lightning_referral() != 0:
        print("post article failed")

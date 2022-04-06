import requests
from common import read_post_common_header_and_params, add_comment_header


def _open_weiguanboyi_post():
    headers, params = read_post_common_header_and_params()
    response = requests.get('https://bbs.byr.cn/article/ParttimeJob/918956', headers=headers, params=params)
    print(response.status_code, response.content)


def _add_weiguanboyi_comment():
    headers = add_comment_header()
    data = {
        'content': '1',
        'id': '918956',
        'subject': 'Re%3A%20%E3%80%90%E5%86%85%E6%8E%A8%E3%80%91%E3%80%90%E5%BE%AE%E8%A7%82%E5%8D%9A%E6%98%93%E3%80%91%E9%87%8F%E5%8C%96%E7%A0%94%E5%8F%91%2F%E7%A0%94%E7%A9%B6%E5%91%98%2F%E5%AE%9E%E4%B9%A0%2FHR'
    }
    response = requests.post('https://bbs.byr.cn/article/ParttimeJob/ajax_post.json', headers=headers, data=data)
    print(response.status_code, response.content)


if __name__ == '__main__':
    _open_weiguanboyi_post()
    _add_weiguanboyi_comment()



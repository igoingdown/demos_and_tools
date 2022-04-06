import requests
from common import read_post_common_header_and_params, add_comment_header


def _open_ms_post():
    headers, params = read_post_common_header_and_params()
    response = requests.get('https://bbs.byr.cn/article/ParttimeJob/918955', headers=headers, params=params)
    print(response.status_code, response.content)


def _add_ms_comment():
    headers = add_comment_header()
    data = {
        'content': '1',
        'id': '918955',
        'subject': 'Re%3A%20%E3%80%90%E5%86%85%E6%8E%A8%E3%80%91%E3%80%90%E5%BE%AE%E8%BD%AF%E3%80%91%E7%AE%97%E6%B3%95%2F%E7%A0%94%E5%8F%91%2F%E4%BA%A7%E5%93%81%2F%E7%A0%94%E7%A9%B6%E5%91%98'
    }

    response = requests.post('https://bbs.byr.cn/article/ParttimeJob/ajax_post.json', headers=headers, data=data)
    print(response.status_code, response.content)


if __name__ == '__main__':
    _open_ms_post()
    _add_ms_comment()



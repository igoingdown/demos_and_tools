import requests
from common import read_post_common_header_and_params, add_comment_header


def _open_bytedance_post():
    headers, params = read_post_common_header_and_params()
    response = requests.get('https://bbs.byr.cn/article/ParttimeJob/918954', headers=headers, params=params)
    print(response.status_code, response.content)


def _add_bytedance_comment():
    headers = add_comment_header()
    data = {
        'content': '1',
        'id': '918954',
        'subject': 'Re%3A%20%E3%80%90%E5%86%85%E6%8E%A8%E3%80%91%E3%80%90%E5%AD%97%E8%8A%82%E3%80%91%E7%94%B5%E5%95%86%E6%96%B9%E5%90%91%E7%A0%94%E5%8F%91%2F%E7%AE%97%E6%B3%95%2F%E8%BF%90%E8%90%A5%2F%E4%BA%A7%E5%93%81'
    }

    response = requests.post('https://bbs.byr.cn/article/ParttimeJob/ajax_post.json', headers=headers, data=data)
    print(response.status_code, response.content)


if __name__ == '__main__':
    _open_bytedance_post()
    _add_bytedance_comment()



import requests
from common import read_post_common_header_and_params, add_comment_header


def _open_anxian_post():
    headers, params = read_post_common_header_and_params()
    response = requests.get('https://bbs.byr.cn/article/ParttimeJob/919307', headers=headers, params=params)
    print(response.status_code, response.content)


def _add_anxian_comment():
    headers = add_comment_header()
    data = {
      'content': '1',
      'id': '919307',
      'subject': 'Re%3A%20%E3%80%90%E5%86%85%E6%8E%A8%E3%80%91%E3%80%90%E5%AE%89%E8%B4%A4%E9%87%8F%E5%8C%96%E3%80%91%E9%87%8F%E5%8C%96%2F%E5%A4%A7%E6%95%B0%E6%8D%AE%2F%E8%BF%90%E7%BB%B4%E7%A0%94%E5%8F%91'
    }

    response = requests.post('https://bbs.byr.cn/article/ParttimeJob/ajax_post.json', headers=headers, data=data)
    print(response.status_code, response.content)


if __name__ == '__main__':
    _open_anxian_post()
    _add_anxian_comment()



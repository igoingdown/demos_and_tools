import requests
from common import read_post_common_header_and_params, add_comment_header

# 新增常量定义
BASE_URL = 'https://bbs.byr.cn/article/ParttimeJob'
POST_ID = '919307'
SUBJECT = 'Re%3A%20%E3%80%90%E5%86%85%E6%8E%A8%E3%80%91%E3%80%90%E5%AE%89%E8%B4%A4%E9%87%8F%E5%8C%96%E3%80%91%E9%87%8F%E5%8C%96%2F%E5%A4%A7%E6%95%B0%E6%8D%AE%2F%E8%BF%90%E7%BB%B4%E7%A0%94%E5%8F%91'

def _open_anxian_post() -> None:
    """获取指定帖子的内容"""
    try:
        headers, params = read_post_common_header_and_params()
        response = requests.get(
            f'{BASE_URL}/{POST_ID}',  # 使用常量拼接URL
            headers=headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()  # 自动处理HTTP错误
        print(f"请求成功，响应长度：{len(response.content)}字节")
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{str(e)}")

def _add_anxian_comment() -> None:
    """添加帖子评论"""
    try:
        headers = add_comment_header()
        response = requests.post(
            f'{BASE_URL}/ajax_post.json',
            headers=headers,
            data={
                'content': '1',
                'id': POST_ID,
                'subject': SUBJECT
            },
            timeout=10
        )
        response.raise_for_status()
        # 尝试解析JSON响应
        json_data = response.json()
        print(f"评论成功，响应数据：{json_data}")
    except requests.exceptions.RequestException as e:
        print(f"评论失败：{str(e)}")
    except ValueError:
        print("响应JSON解析失败")


if __name__ == '__main__':
    _open_anxian_post()
    _add_anxian_comment()



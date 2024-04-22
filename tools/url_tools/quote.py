import argparse
import urllib.parse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="脚本描述信息")
    # 添加参数
    parser.add_argument("-u", "--user_name", help="用户名", type=str, default='hzplszl')
    parser.add_argument("-p", "--pwd", help="pwd", type=str, default='lslhcqy')
    parser.add_argument("-b", "--board", help="board_name", type=str, default='Advertising')
    parser.add_argument("-t", "--tiezi", help="帖子id", type=int, default=2087585)
    params = parser.parse_args()
    q = 'content=a%0A&id=1&subject=Re%253A%2520%25E3%2580%2590%25E5%2586%2585%25E6%258E%25A8%25E3%2580%2591%25E3%2580%2590%25E5%25AE%2589%25E8%25B4%25A4%25E9%2587%258F%25E5%258C%2596%25E3%2580%2591%25E9%2587%258F%25E5%258C%2596%252F%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE%252F%25E8%25BF%2590%25E7%25BB%25B4%25E7%25A0%2594%25E5%258F%2591'
    decoded_query = urllib.parse.parse_qsl(q)
    print(decoded_query[2][1])



    encoded_string = decoded_query[2][1]
    decoded_string = urllib.parse.unquote(encoded_string)
    print(decoded_string)

    title = 'Re: 【内推】【安贤量化】量化/大数据/运维研发'
    params = {'content': 'a\n', 'id': 1, 'subject': urllib.parse.quote(title)}
    encoded_query_string = urllib.parse.urlencode(params)
    print(encoded_query_string)
    print(q)


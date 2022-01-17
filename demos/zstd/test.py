#!/usr/bin/python3

import zstd
"""
===============================================================================
author: 赵明星
desc:   测试 zstd 压缩算法。
===============================================================================
"""


def foo():
    o_data = b"aaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbxxxxxxxxxxxxxxxxxxxbbbbbbbbbbbbbbbbbbbbbbbxxxxxxxxxxxxxxxxxxbbbbbbbbbbbbbbbbbbaahello,word"
    d_data = o_data.decode("utf-8")
    compressed = zstd.ZSTD_compress(o_data)
    """
    utf8_str = compressed.decode("utf-8")
    """
    for i in compressed:
        print(i)
    print(compressed)


if __name__ == '__main__':
    foo()

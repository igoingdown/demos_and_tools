import time
from common import get_rand_int
from login import _login
from find_parttime_job import _find_parttime_job
from anxianlianghua import _open_anxian_post, _add_anxian_comment
from ms_stca import _open_ms_post, _add_ms_comment
from bytedance_job import _open_bytedance_post, _add_bytedance_comment
from weiguanboyi import _open_weiguanboyi_post, _add_weiguanboyi_comment


def main():
    _login()
    time.sleep(get_rand_int(5, 10))
    _find_parttime_job()
    time.sleep(get_rand_int(5, 10))
    _open_anxian_post()
    time.sleep(get_rand_int(1, 4))
    _add_anxian_comment()

    time.sleep(get_rand_int(5, 10))
    _open_bytedance_post()
    time.sleep(get_rand_int(1, 4))
    _add_bytedance_comment()

    '''
    time.sleep(get_rand_int(5, 10))
    _open_ms_post()
    time.sleep(get_rand_int(1, 4))
    _add_ms_comment()
    '''

    time.sleep(get_rand_int(5, 10))
    _open_weiguanboyi_post()
    time.sleep(get_rand_int(1, 4))
    _add_weiguanboyi_comment()


if __name__ == '__main__':
    main()

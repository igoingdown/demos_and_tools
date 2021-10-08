#!/usr/bin/python3

"""
===============================================================================
author: 赵明星
desc:   删除指定目录下的指定文件名的所有文件
===============================================================================
"""

import os
import shutil


def delete_output(work_dir):
    for parent, dir_names, _ in os.walk(work_dir, followlinks=False):
        for dir_name in dir_names:
            dest_path = os.path.join(parent, dir_name)
            if dir_name == "output":
                print(dest_path)
                shutil.rmtree(dest_path)
                continue
            delete_output(dest_path)


if __name__ == "__main__":
    delete_output(os.getcwd())

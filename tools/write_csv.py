#!/usr/bin/python3
import csv


def write_csv(file_path, header, data):

    # 打开 csv 文件并写入数据
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

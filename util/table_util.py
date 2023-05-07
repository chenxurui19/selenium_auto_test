# -*- coding: utf-8 -*-
# @Time    : 2023/5/6 18:42
# @Author  : CXRui
# @File    : table_util.py
# @Description
import csv
from datetime import datetime


def wirte_csv(file, data, mode='a'):
    with open(file, mode) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

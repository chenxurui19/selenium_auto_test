# -*- coding: utf-8 -*-
# @Time    : 2023/5/7 22:09
# @Author  : CXRui
# @File    : util.py
# @Description :
import os
import shutil


def mkdir_empty_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)
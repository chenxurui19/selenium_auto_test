# -*- coding: utf-8 -*-
# @Time    : 2023/5/7 21:44
# @Author  : CXRui
# @File    : config.py
# @Description : 保存全局变量

class GlobalVar:

    BROWER_TYPE = "safari"

    @staticmethod
    def set_brower_type(brower_type):
        GlobalVar.BROWER_TYPE = brower_type

    @staticmethod
    def get_brower_type():
        return GlobalVar.BROWER_TYPE

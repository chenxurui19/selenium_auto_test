# -*- coding: utf-8 -*-
# @Time    : 2023/5/6 13:54
# @Author  : CXRui
# @File    : login_page.py
# @Description :
import time

import pytest

from common.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):

    login_page_url = "http://www.chenxurui.cn/admin"
    username_input_box = (By.NAME, "username")    # 用户名输入框
    password_input_box = (By.NAME, "password")     # 密码输入框
    login_btn = (By.XPATH, '//button[contains(@class, "submit")]')  # 登录按钮
    login_sucess = (By.XPATH, '//p[contains(text(), "欢迎登录")]')       # 登录成功标识

    def __init__(self, driver):
        super().__init__(driver)

    def open_login_page(self):
        self.open_url(self.login_page_url)

    def send_username(self, text):
        """
        输入用户名
        :param text:
        :return:
        """
        self.send_keys(self.username_input_box, text)

    def send_password(self, text):
        """
        输入密码
        :return:
        """
        self.send_keys(self.password_input_box, text)

    def click_login(self):
        self.click_element(self.login_btn)

    def check_login_success(self):
        return self.get_existed(self.login_sucess)

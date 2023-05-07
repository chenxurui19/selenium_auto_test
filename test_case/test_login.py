# -*- coding: utf-8 -*-
# @Time    : 2023/5/6 18:42
# @Author  : CXRui
# @File    : test_login.py
# @Description :
import logging
import time
from datetime import datetime
import pytest
from page.login_page import LoginPage
from common.browser_driver import BrowserDriver

global login_page


@pytest.mark.usefixtures("driver_setup")
class TestLogin:
    @pytest.fixture()
    def init_setup(self):
        global login_page
        logging.info(self.driver)
        login_page = LoginPage(self.driver)
        logging.info("前置：打开url网址")
        login_page.open_login_page()     # 打开url网址

        yield

        logging.info("后置：测试结束")

    @pytest.mark.test_login_success
    def test_login_success(self, init_setup):
        global login_page
        login_page.implicitly_wait(10)
        logging.info("测试：输入账号")
        login_page.send_username("admin")
        logging.info("测试：输入密码")
        login_page.send_password("admin")

        # 点击登录
        login_page.click_login()
        time.sleep(3)   # 等待页面跳转，不等待可能会报异常
        assert login_page.check_login_success(), "登录失败"


if __name__ == '__main__':
    pytest.main(["-vs", "-m", "test_login_success", "--count", "100", "--html", "../html_report/html_report.html"])

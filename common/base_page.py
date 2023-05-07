# -*- coding: utf-8 -*-
# @Time    : 2023/5/6 09:57
# @Author  : CXRui
# @File    : base_page.py
# @Description : 二次封装selenium
import logging
import time
from telnetlib import EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator):
        """
        查找单个元素
        :param locator: 元组：(定位方法, 定位文本)，比如(By.XPATH, '//*[text()="视频"]')
        :return:
        """
        method = locator[0]
        value = locator[1]
        return self.driver.find_element(method, value)

    def find_elements(self, locator):
        """
        查找所有元素
        :param locator: 元组：(定位方法, 定位文本)，比如(By.XPATH, '//*[text()="视频"]')
        :return:
        """
        method = locator[0]
        value = locator[1]
        return self.driver.find_elements(method, value)

    def open_url(self, url):
        """
        打开网站
        :param url: 网站地址
        :return:
        """
        self.driver.get(url)

    def get_url(self):
        """
        获取当前页面的URL地址
        :return:
        """
        return self.driver.current_url

    def get_title(self):
        """
        获取当前页面的标题
        :return:
        """
        return self.driver.title

    def get_handler(self):
        """
        获取当前窗口句柄
        :return:
        """
        return self.driver.current_window_handle

    def maximize_windows(self):
        """
        窗口最大化
        :return:
        """
        self.driver.maximize_window()

    def minximize_windows(self):
        """
        窗口最小化
        :return:
        """
        self.driver.minimize_window()

    def refresh(self, url=None):
        """
        刷新页面
        :param url: 页面网址
        :return: None
        """
        if url is None:
            self.driver.refresh()
        else:
            self.driver.get(url)

    def back_up(self):
        """
        浏览器 后退
        :return:
        """
        self.driver.back()

    def go_forward(self):
        """
        浏览器 前进
        :return:
        """
        self.driver.forward()

    def close_browser(self):
        """
        关闭窗口或者标签页
        :return:
        """
        self.driver.close()

    def quit(self):
        """
        退出 浏览器驱动
        :return: None
        """
        self.driver.quit()

    def click_element(self, locator):
        """
        鼠标点击元素
        :param locator: 元组：(定位方法, 定位文本)，比如(By.XPATH, '//*[text()="视频"]')
        :return:
        """
        self.find_element(locator).click()

    def clear_input_box(self, locator):
        """
        清空选定的输入框
        :return:
        """
        self.find_element(locator).clear()

    def send_keys(self, locator, text):
        """
        选定输入框，输入文本
        :return:
        """
        self.find_element(locator).send_keys(text)

    def select_by_index(self, locator, index):
        """
        index的方式 点击选择复选框，单选按钮，甚至下拉框
        :param locator: 元组：(定位方法, 定位文本)，比如(By.XPATH, '//*[text()="视频"]')
        :param index: 标签 下标值（int number）
        :return:
        """
        el = self._locator_element(locator)
        Select(el).select_by_index(index)

    def get_selected(self, locator):
        """
        得到元素的选定状态
        :param locator: 元组：(定位方法, 定位文本)，比如(By.XPATH, '//*[text()="视频"]')
        :return: bool
        """
        return self.find_element(locator).is_selected()

    def get_existed(self, locator):
        """
        判断元素是否存在
        :param locator: 元组：(定位方法, 定位文本)，比如(By.XPATH, '//*[text()="视频"]')
        :return: 如果存在返回控件，不存在返回False
        """
        try:
            el = self.find_element(locator)
            return el
        except Exception as e:
            return False

    def get_displayed(self, locator):
        """
        获取元素的显示状态
        :param locator: 元组：(定位方法, 定位文本)，比如(By.XPATH, '//*[text()="视频"]')
        :return: bool
        """
        return self.find_element(locator).is_enabled()

    def get_enabled(self, locator):
        """
        判断元素是否可点击
        :param locator: 元组：(定位方法, 定位文本)，比如(By.XPATH, '//*[text()="视频"]')
        :return: bool
        """
        return True if self.find_element(locator).is_enabled() else False

    def accept_alert(self):
        """
        接受 Alert 警告框
        :return:
        """
        self._base_driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        取消 Alert 警告框
        :return:
        """
        self._base_driver.switch_to.alert.dismiss()

    def get_alert_text(self):
        """
        获取 Alert弹框的文本内容
        :return:
        """
        text = self._base_driver.switch_to.alert.text
        return text

    def switch_to_frame(self, locator):
        """
        进入 iframe 框架
        :param locator: 元组：(定位方法, 定位文本)，比如(By.XPATH, '//*[text()="视频"]')
        :return:
        """
        el = self.find_element(locator)
        self.driver.switch_to.frame(el)

    def explicitly_wait(self, locator, timeout=10):
        """
        显示等待，超时未找到就报异常
        :param locator: 元组：(定位方法, 定位文本)，比如(By.XPATH, '//*[text()="视频"]')
        :param timeout: 超时时间
        :return:
        """
        el = self.find_element(locator)
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(el))
        return el

    def implicitly_wait(self, timeout):
        """
        隐式等待，全局控件有超时未找到就报异常
        :param timeout:
        :return:
        """
        self.driver.implicitly_wait(timeout)

    def move_to(self, locator):
        """
        鼠标悬停
        :param locator: 元组：(定位方法, 定位文本)，比如(By.XPATH, '//*[text()="视频"]')
        :return:
        """
        el = self.find_element(locator)
        ActionChains(self.driver).move_to_element(el).perform()

    def save_screenshot(self, filename):
        """
        屏幕截图
        :param filename: 截图保存的路径
        :return:
        """
        self.driver.save_screenshot(filename)

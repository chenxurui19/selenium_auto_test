# -*- coding: utf-8 -*-
# @Time    : 2023/5/7 18:10
# @Author  : CXRui
# @File    : conftest.py
# @Description :
import os
import pytest
from datetime import datetime
from util.util import mkdir_empty_dir
from config.config import GlobalVar
from common.browser_driver import BrowserDriver
from selenium import webdriver
from py.xml import html

src = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 当前的目录详细位置
datetime_format = "%Y-%m-%d_%H.%M.%S"  # 时间格式化
driver = None


@pytest.fixture(scope="class")
def driver_setup(request):
    """
    :param request:
    :return:
    """
    global driver, brower_type
    brower_type = cmd_brower_type(request)
    GlobalVar.set_brower_type(brower_type)

    if brower_type == BrowserDriver.CHROME:
        driver = webdriver.Chrome()
    elif brower_type == BrowserDriver.FIREFOX:
        driver = webdriver.Firefox()
    elif brower_type == BrowserDriver.IE:
        driver = webdriver.Ie()
    elif brower_type == BrowserDriver.EDGE:
        driver = webdriver.Edge()
    elif brower_type == BrowserDriver.SAFARI:
        driver = webdriver.Safari()
    else:
        raise Exception("This browser is not supported")
    # 设置隐式等待为10s
    driver.implicitly_wait(10)

    report_dir = f"{src}/html_report"  # html_report不存在就创建，否则先删除再创建，防止占用太多磁盘空间
    mkdir_empty_dir(report_dir)
    request.cls.driver = driver

    yield driver

    try:
        driver.quit()
    except Exception as e:
        pass


# ----------------------------配置html_report报告--------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    html_report用法：
    https://pytest-html.readthedocs.io/en/latest/index.html
    https://blog.csdn.net/FloraCHY/article/details/125521949
    :param item:测试用例对象
　　 :param call:测试用例的测试步骤
　　         执行完常规钩子函数返回的report报告有个属性叫report.when
            先执行when=’setup’ 返回setup 的执行结果
            然后执行when=’call’ 返回call 的执行结果
            最后执行when=’teardown’返回teardown 的执行结果
    :return:
    钩子函数：#此钩子函数在setup(初始化的操作)，call（测试用例执行时），teardown（测试用例执行完毕后的处理）都会执行一次，
    跟@pytest.mark.hookwrapper一样
    作用：
    （1）可以获取到测试用例不同执行阶段的结果（setup，call，teardown）
    （2）可以获取钩子方法的调用结果（yield返回一个result对象）和调用结果的测试报告（返回一个report对象）
    每个测试用例执行后，制作测试报告
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = get_description(item)
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup" or report.when == "teardown":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            html_path = make_html_report_path(report.nodeid)
            name = datetime.now().strftime(datetime_format)
            screenshot_name = f"{name}.png"  # 截图统一名称
            screenshot_path, screenshot_html = save_screenshot(html_path, screenshot_name)
            extra.append(pytest_html.extras.html(screenshot_html))


def save_screenshot(html_path, name):
    """
    保存截图到html报告
    :param html_path: html保存路径
    :param name: 截图名称
    :return:
    """
    global driver
    screenshot_path = os.path.join(html_path, name)
    driver.save_screenshot(screenshot_path)
    html = '<div><img src="{}" alt="screenshot" width="180" height="320"' \
           'onclick="window.open(this.src)" align="right"/></div>'.format(screenshot_path)
    return screenshot_path, html


def pytest_html_report_title(report):
    """
    更改html_report标题
    :param report:
    :return:
    """
    report.title = "自动化测试报告"


def pytest_configure(config):
    """
    给环境表添加开始时间、测试包、以及脚本开发者名字
    :param config:
    :return:
    """
    config._metadata["测试开始时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config._metadata["测试浏览器"] = GlobalVar.get_brower_type()


def pytest_html_results_summary(prefix, summary, postfix):
    """
    from py.xml import html
    :param prefix:
    :param summary:
    :param postfix:
    :return:
    """
    prefix.extend([html.p("测试开发：Chen Xurui")])


def get_description(item):
    """
    获取用例函数的注释
    :param item:
    :return:
    """
    doc = str(item.function.__doc__)
    index = doc.find(":param")
    if index == -1:
        index = doc.find(":return:")
    if index != -1:
        return doc[:index]
    else:
        return doc


def make_html_report_path(nodeid):
    """
    创建保存失败截图和日志的文件目录
    :param nodeid:
    :return:
    """
    base_path = nodeid.replace("()", "").replace("::::", "::").replace("::", "/")
    html_path = "../html_report/{}".format(base_path)
    if not os.path.exists(html_path):
        os.makedirs(html_path)
    return html_path


# ----------------------------注册命令行参数--------------------------------
def pytest_addoption(parser):
    """
    注册命令行参数
    :param parser:
    :return:
    """
    parser.addoption("--brower_type", action="store", default="safari", help="浏览器类型：chrome、firefox、ie、edge、safari")


# ----------------------------命令行获取参数--------------------------------
def cmd_brower_type(request):
    """
    脚本获取命令行参数的接口：浏览器类型
    :param request:
    :return:
    """
    value = request.config.getoption("--brower_type")
    return value

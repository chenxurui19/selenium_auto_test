# selenium_auto_test
这是一款基于Pytest+Selenium二次封装的Web ui自动化框架，遵循PO模式编写用例，测试失败会自动截图，测试结束会生成详细可观的HTML报告
## 效果演示
![image_1.png](exampe_image%2Fimage_1.png)
## 准备工作
### 本地环境搭建
命令行执行
```angular2html
pip install -r requirements.txt
```
如安装过慢，可以加-i指定国内镜像源，如豆瓣
```angular2html
pip install -r requirements.txt -i https://pypi.douban.com/simple/
```
## pycharm启动示例
按照如下配置，点击执行按钮即可
![pycharm.png](exampe_image%2Fpycharm.png)
-m：需要执行的标签，例如案例setting_wifi，如需同时执行标签A和标签B，则可填写-m "A or B"，如需要执行同时满足标签A和B，则可填写-m "A and B"
--count：需要执行的次数，例如--count=100，就是执行100次
--html：html_report生成地址，一般填写--html=../html_report/html_report.html即可
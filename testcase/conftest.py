import pytest
from util_tools.logs_util.recordlog import logs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config.setting import browser_type, WAIT_TIME

"""
conftest.py文件是一个单独存放的测试夹具，pytest会自动搜索conftest.py文件并执行其中的测试夹具。
可以创建多个conftest.py文件，每个conftest.py文件会对其所在目录及其子目录下的测试模块生效。
在不同模块的测试中需要用到conftest.py的前后置功能时，不需要做任何的import导入操作
作用:可以在不同的py文件中使用同一个fixture函数
"""


@pytest.fixture(scope='function', autouse=True)
def info_output():
    logs.info('——————测试用例开始执行——————')
    yield
    logs.info('——————测试用例结束执行——————')


@pytest.fixture(scope='function')
def get_driver():
    """初始化浏览器对象"""
    browser_mapping = {
        'chrome': lambda: webdriver.Chrome(service=Service(r"D:\chromedriver-win64\chromedriver.exe")),
        # 默认使用chrome，注意，需安装chrome驱动
        'edge': lambda: webdriver.Edge(service=Service(r"D:\edgedriver-win64\msedgedriver.exe")),
        # 默认使用edge，注意，需安装edge驱动
        'firefox': lambda: webdriver.Firefox(service=Service(r"D:\geckodriver-win64\geckodriver.exe")),
        # 默认使用firefox，注意，需安装firefox驱动
    }
    driver = browser_mapping[browser_type.lower()]()

    # 设置一个全局的隐式等待时间
    driver.implicitly_wait(WAIT_TIME)
    # 最大化浏览器窗口
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def registered_user():
    """预置一个已存在的用户，供注册失败/登录等场景使用"""
    return {
        "username": "lisi",
        "password": "dongli1314",
        "email": "3298535595@qq.com",
        "question": "我最喜爱的电影？",
        "answer": "1"
    }

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.setting import browser_type, WAIT_TIME, DRIVER_PATH
from pageObject.login_page.login_page import LoginPage
from util_tools.basePage import BasePage
from util_tools.logs_util.recordlog import logs

"""
conftest.py文件是一个单独存放的测试夹具，pytest会自动搜索conftest.py文件并执行其中的测试夹具。
可以创建多个conftest.py文件，每个conftest.py文件会对其所在目录及其子目录下的测试模块生效。
在不同模块的测试中需要用到conftest.py的前后置功能时，不需要做任何的import导入操作
作用:可以在不同的py文件中使用同一个fixture函数
"""


@pytest.fixture(scope='function', autouse=True)
@allure.title('测试用例执行')
def info_output():
    logs.info('——————测试用例开始执行——————')
    yield
    logs.info('——————测试用例结束执行——————')


def init_driver():
    """初始化浏览器对象"""
    service = Service(DRIVER_PATH[browser_type.lower()])
    browser_mapping = {
        'chrome': lambda: webdriver.Chrome(service=service),
        'edge': lambda: webdriver.Edge(service=service),
        'firefox': lambda: webdriver.Firefox(service=service),
    }
    return browser_mapping[browser_type.lower()]()


@pytest.fixture(scope='class')
@allure.title('初始化浏览器对象')
def get_driver():
    """初始化浏览器对象"""
    driver = init_driver()
    # 设置一个全局的隐式等待时间
    driver.implicitly_wait(WAIT_TIME)
    # 最大化浏览器窗口
    # driver.maximize_window()
    yield driver
    driver.quit()


# 登录状态的前置应用
@pytest.fixture(scope='class')
@allure.title('设置登录状态')
def login_driver(get_driver):
    driver = get_driver
    login_page = LoginPage(driver)
    login_page.login("admin", "admin1314")
    # 等顶部出现"用户中心"链接，说明登录已完成、页面已跳转
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.LINK_TEXT, "用户中心"))
    )
    return driver


# 未登录状态的前置应用
@pytest.fixture()
@allure.title('设置未登录状态')
def not_login_driver():
    global driver
    driver = init_driver()
    driver.implicitly_wait(WAIT_TIME)
    yield driver
    driver.quit()


# 钩子函数,每个测试用例执行之后执行
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    # 只在用例本体失败时截图
    if result.when == 'call' and result.failed and not hasattr(result, 'wasxfail'):
        driver = (
                item.funcargs.get('get_driver')
                or item.funcargs.get('not_login_driver')
                or item.funcargs.get('login_driver')
        )
        if driver:
            with allure.step('测试失败截图'):
                BasePage(driver).attach_screenshot('失败截图')

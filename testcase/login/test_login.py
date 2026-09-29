from time import sleep
import pytest
from selenium.common import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from util_tools.handle_data.readYaml import read_yaml
from util_tools.handle_data.operateJson import read_json
from selenium.webdriver.common.by import By
from pageObject.login_page.login_page import LoginPage
from util_tools.handle_data.operateExcel import ExcelDataReader


class TestLogin:

    # # 登录成功,读取yaml文件的
    # @pytest.mark.parametrize("data", read_yaml('D:/Test/WEB/data/login.yaml'))
    # def test_login_success(self, get_driver, data):
    #     username, password = data
    #     login_page = LoginPage(get_driver)
    #     login_page.login(username, password)
    #
    #     # 断言登录结果
    #     login_page.is_element_present(login_page.assert_result)
    #     sleep(3)
    #
    # 登录成功,读取json文件的
    @pytest.mark.parametrize("data", read_json('D:/Test/WEB/data/login_success.json'))
    def test_login_success(self, get_driver, data):
        username, password = data
        login_page = LoginPage(get_driver)
        login_page.login(username, password)

        # 断言登录结果
        login_page.assert_is_element_present(login_page.assert_result)
        sleep(3)

    # # 登录成功,读取excel文件的
    # @pytest.mark.parametrize("data", ExcelDataReader('D:/Test/WEB/data/login_testdata.xlsx').read_multiple_rows())
    # def test_login_success(self, get_driver, data):
    #     username, password = data
    #     login_page = LoginPage(get_driver)
    #     login_page.login(username, password)
    #
    #     # 断言登录结果
    #     login_page.is_element_present(login_page.assert_result)
    #     sleep(3)

    # 登录失败,读取json文件的
    @pytest.mark.parametrize("data", read_json('D:/Test/WEB/data/login_failed.json'))
    def test_login_failed(self, get_driver, data):
        username, password = data
        login_page = LoginPage(get_driver)
        login_page.login(username, password)

        # 断言登录结果
        WebDriverWait(get_driver, 10).until(
            EC.title_contains("系统提示")  # type: ignore
        )
        login_page.assert_title('系统提示')
        sleep(3)

    # # 登录失败
    # def test_login_fail(self, get_driver):
    #     login_page = LoginPage(get_driver)
    #     login_page.login("lisi", "dongli13142")
    #     # 断言登录结果
    #     assert "重新登录" in get_driver.page_source
    #     sleep(3)

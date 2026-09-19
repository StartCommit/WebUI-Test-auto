from time import sleep
import pytest
from util_tools.handle_data.readYaml import read_yaml
from util_tools.handle_data.operateJson import read_json
from selenium.webdriver.common.by import By
from pageObject.login_page.login_page import LoginPage


class TestLogin:

    # 登录成功,读取yaml文件的
    @pytest.mark.parametrize("data", read_yaml('D:\Test\WEB\data\login.yaml'))
    def test_login_success(self, get_driver, data):
        username, password = data
        login_page = LoginPage(get_driver)
        login_page.login(username, password)

        # 断言登录结果
        success_text = get_driver.find_element(By.XPATH, '//*[@id="ECS_MEMBERZONE"]/font/font')
        assert success_text.text != ''
        sleep(2)

    # 登录成功,读取json文件的
    @pytest.mark.parametrize("data", read_json('D:\Test\WEB\data\login.json'))
    def test_login_success(self, get_driver, data):
        username, password = data
        login_page = LoginPage(get_driver)
        login_page.login(username, password)

        # 断言登录结果
        success_text = get_driver.find_element(By.XPATH, '//*[@id="ECS_MEMBERZONE"]/font/font')
        assert success_text.text != ''
        sleep(2)

    # 登录失败
    def test_login_fail(self, get_driver):
        login_page = LoginPage(get_driver)
        login_page.login("lisi", "dongli13142")
        # 断言登录结果
        assert "重新登录" in get_driver.page_source
        sleep(3)

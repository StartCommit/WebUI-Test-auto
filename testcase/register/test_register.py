from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pageObject.register_page.register_page import RegisterPage
from util_tools.handle_data.readYaml import read_yaml
import pytest


class TestRegister:

    # # 注册成功,死数据
    # def test_register_success(self):
    #     register_page = RegisterPage(self.driver)
    #     register_page.register("lisi234", "lisi234@163.com", "dongli1314", "dongli1314",
    #                            "lisi234@163.com", "123456", "13912345678", "13912345678", "13912345678",
    #                            "我最喜爱的电影？", "1")
    #     sleep(3)
    #     # 断言登录结果
    #     success_text = self.driver.find_element(By.XPATH, '//*[@id="ECS_MEMBERZONE"]/font/font')
    #     assert "lisi234" in success_text.text

    # 注册失败,死数据
    # def test_register_fail(self):
    #     register_page = RegisterPage(self.driver)
    #     register_page.register("lisi234", "lisi234@163.com", "dongli1314", "dongli1314",
    #                            "lisi234@163.com", "123456", "13912345678", "13912345678", "13912345678",
    #                            "我最喜爱的电影？", "1")
    #     sleep(3)
    #     # 断言登录结果
    #     assert "lisi23" not in self.driver.page_source  # 没登录成功

    # 注册成功,读取yaml文件的
    @pytest.mark.parametrize("data", read_yaml('D:/Test/WEB/data/register_success.yaml'))
    def test_register_success(self, get_driver, data):
        register_page = RegisterPage(get_driver)
        # 如果使用*data解包数据，data的元素必须跟click_register方法中的参数一致
        register_page.register(*data)
        # 断言登录结果
        WebDriverWait(get_driver, 5).until(
            ec.presence_of_element_located(register_page.assert_result)
        )
        register_page.assert_is_element_present(register_page.assert_result) #断言元素存在，存在则返回true

    # 注册成功,读取yaml文件的
    @pytest.mark.parametrize("data", read_yaml('D:/Test/WEB/data/register_failed.yaml'))
    def test_register_fail(self, get_driver, data):
        register_page = RegisterPage(get_driver)
        # 如果使用*data解包数据，data的元素必须跟click_register方法中的参数一致
        register_page.register(*data)
        # 断言登录结果
        register_page.assert_element_not_visible(register_page.assert_result) #断言元素不存在，不存在则返回true

    # 跳转登录功能
    def test_check_skip_login(self, get_driver):
        register_page = RegisterPage(get_driver)
        register_page.skip_login_button()
        # 断言结果
        assert register_page.current_url == 'http://localhost/ecshop/user.php?act=login'
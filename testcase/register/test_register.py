import allure
import pytest
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from pageObject.register_page.register_page import RegisterPage
from util_tools.handle_data.readYaml import read_yaml

@pytest.mark.run(order=1)
@allure.feature("注册模块")
class TestRegister:

    # 注册成功,读取yaml文件的
    @allure.story('用户注册成功')
    @allure.title('注册成功')
    @pytest.mark.parametrize("data", read_yaml('register_success.yaml'))
    def test_register_success(self, not_login_driver, data):
        register_page = RegisterPage(not_login_driver)
        # 如果使用*data解包数据，data的元素必须跟click_register方法中的参数一致
        register_page.register(*data)
        # 断言登录结果
        WebDriverWait(not_login_driver, 10).until(
            ec.presence_of_element_located(register_page.assert_result)
        )
        register_page.assert_is_element_present(register_page.assert_result)  # 断言元素存在，存在则返回true

    # 注册成功,读取yaml文件的
    @allure.story('用户注册失败')
    @allure.title('注册失败')
    @pytest.mark.parametrize("data", read_yaml('register_failed.yaml'))
    def test_register_fail(self, not_login_driver, data):
        register_page = RegisterPage(not_login_driver)
        # 如果使用*data解包数据，data的元素必须跟click_register方法中的参数一致
        register_page.register(*data)
        # 断言登录结果
        register_page.assert_element_not_visible(register_page.assert_result)  # 断言元素不存在，不存在则返回true

    # 跳转登录功能
    @allure.story('用户注册页面跳转登录功能')
    @allure.title('注册页面跳转登录')
    def test_check_skip_login(self, not_login_driver):
        register_page = RegisterPage(not_login_driver)
        register_page.skip_login_page()
        # 断言结果
        assert 'user.php' in register_page.current_url and 'act=login' in register_page.current_url

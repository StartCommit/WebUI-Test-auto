import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pageObject.login_page.login_page import LoginPage
from util_tools.handle_data.operateExcel import ExcelDataReader
from util_tools.handle_data.operateJson import read_json
from util_tools.handle_data.readYaml import read_yaml


@allure.feature("登录模块")
class TestLogin:
    # # 登录成功,读取yaml文件的
    @allure.story('用户登录成功')  # 测试用例标签
    @allure.title('登录成功-读取yaml文件数据')  # 测试用例标题
    @pytest.mark.parametrize("data", read_yaml('login_success.yaml'))
    def test_login_success_01(self, not_login_driver, data):
        username, password = data
        login_page = LoginPage(not_login_driver)
        login_page.login(username, password)

        # 断言登录结果
        login_page.assert_is_element_present(login_page.assert_result)

    # 登录成功,读取json文件的
    @allure.story('用户登录成功')
    @allure.title('登录成功-读取json文件数据')  # 测试用例标题
    @allure.link("https://www.baidu.com", "百度")  # 测试用例链接
    @allure.description('测试登录功能-成功')  # 测试用例描述
    @allure.severity(allure.severity_level.CRITICAL)  # 测试用例等级
    @pytest.mark.parametrize("data", read_json('login_success.json'))
    def test_login_success_02(self, not_login_driver, data):
        username, password = data
        login_page = LoginPage(not_login_driver)
        login_page.login(username, password)
        # 添加附件,用于在测试报告中添加附件，例如日志文件，截图，通过allure.attach.file()添加，在函数内部使用，不是使用装饰器
        # allure.attach.file(
        #     r'D:\Test\WEB\requirements.txt',
        #     name='依赖',
        #     attachment_type=allure.attachment_type.TEXT
        # )
        # # 读取文件乱码时使用with open()打开文件，并且指定编码格式
        # with open(r'D:\Test\WEB\requirements.txt', 'r', encoding='utf-16') as f:
        #     content = f.read()
        # allure.attach(content, name='依赖', attachment_type=allure.attachment_type.TEXT)
        # 断言登录结果
        login_page.assert_is_element_present(login_page.assert_result)

    # # 登录成功,读取excel文件的
    @allure.story('用户登录成功')
    @allure.title('登录成功-读取xlsx文件数据')
    @pytest.mark.parametrize("data", ExcelDataReader('login_testdata.xlsx').read_multiple_rows())
    def test_login_success_03(self, not_login_driver, data):
        username, password = data
        login_page = LoginPage(not_login_driver)
        login_page.login(username, password)

        # 断言登录结果
        login_page.assert_is_element_present(login_page.assert_result)

    # 登录失败,读取json文件的
    @allure.story('用户登录失败')
    @allure.title('登录失败')
    @allure.severity(allure.severity_level.BLOCKER)  # 测试用例等级
    @pytest.mark.parametrize("data", read_json('login_failed.json'))
    def test_login_failed(self, not_login_driver, data):
        username, password = data
        login_page = LoginPage(not_login_driver)
        login_page.login(username, password)

        # 断言登录结果
        WebDriverWait(not_login_driver, 10).until(
            EC.title_contains("系统提示")  # type: ignore
        )
        login_page.assert_title('系统提示')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from pageObject.register_page.register_page import RegisterPage


class TestRegister:

    def setup_method(self):
        # webdriver初始化
        self.driver = webdriver.Chrome(service=Service(r"D:\chromedriver-win64\chromedriver.exe"))

    # 注册成功
    def test_register_success(self):
        register_page = RegisterPage(self.driver)
        register_page.register("lisi234", "lisi234@163.com", "dongli1314", "dongli1314",
                               "lisi234@163.com", "123456", "13912345678", "13912345678", "13912345678",
                               "我最喜爱的电影？", "1")
        sleep(3)
        # 断言登录结果
        success_text = self.driver.find_element(By.XPATH, '//*[@id="ECS_MEMBERZONE"]/font/font')
        assert "lisi234" in success_text.text

    # 注册失败
    def test_register_fail(self):
        register_page = RegisterPage(self.driver)
        register_page.register("lisi234", "lisi234@163.com", "dongli1314", "dongli1314",
                               "lisi234@163.com", "123456", "13912345678", "13912345678", "13912345678",
                               "我最喜爱的电影？", "1")
        sleep(3)
        # 断言登录结果
        assert "lisi23" not in self.driver.page_source  # 没登录成功

    def teardown_method(self):
        self.driver.quit()

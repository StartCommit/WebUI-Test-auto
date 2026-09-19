from selenium.webdriver.common.by import By
from util_tools.basePage import BasePage


class LoginPage(BasePage):
    # url
    url = "http://localhost/ecshop/user.php"
    # 用户名
    username = (By.NAME, "username")
    # 密码
    password = (By.NAME, "password")
    # 登录按钮
    submit = (By.NAME, "submit")

    # 登录操作
    def login(self, user_name, pass_word):
        self.open_url(self.url)
        # 输入用户名
        self.send_keys(self.username, user_name)
        # 输入密码
        self.send_keys(self.password, pass_word)
        # 点击登录按钮
        self.click(self.submit)

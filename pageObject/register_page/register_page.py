from selenium.webdriver.common.by import By
from util_tools.basePage import BasePage


class RegisterPage(BasePage):
    # url
    url = "http://localhost/ecshop/user.php?act=register"
    # 用户名
    user_name = (By.NAME, "username")
    # 邮箱
    email = (By.NAME, "email")
    # 密码
    password = (By.NAME, "password")
    # 确认密码
    confirm_password = (By.NAME, "confirm_password")
    # MSN
    msn = (By.NAME, "extend_field1")
    # QQ
    qq = (By.NAME, "extend_field2")
    # 公办电话
    public_telephone = (By.NAME, "extend_field3")
    # 家庭电话
    family_telephone = (By.NAME, "extend_field4")
    # 手机
    phone = (By.NAME, "extend_field5")
    # 下拉框问题
    question = (By.NAME, "sel_question")
    # 问题答案
    answer = (By.NAME, "passwd_answer")
    # 我接受
    agree = (By.NAME, "agreement")
    # 注册按钮
    submit = (By.NAME, "Submit")

    # 注册操作
    def register(self, user_name, email, password, confirm_password, msn, qq, public_telephone, family_telephone, phone,
                 question_text, question_answer):
        self.open_url(self.url)
        # 输入用户名
        self.send_keys(self.user_name, user_name)
        # 输入邮箱
        self.send_keys(self.email, email)
        # 输入密码
        self.send_keys(self.password, password)
        # 输入确认密码
        self.send_keys(self.confirm_password, confirm_password)
        # 输入MSN
        self.send_keys(self.msn, msn)
        # 输入QQ
        self.send_keys(self.qq, qq)
        # 输入公办电话
        self.send_keys(self.public_telephone, public_telephone)
        # 输入家庭电话
        self.send_keys(self.family_telephone, family_telephone)
        # 输入手机
        self.send_keys(self.phone, phone)
        # 选择问题
        self.select_by_text(self.question, question_text)
        # 输入答案
        self.send_keys(self.answer, question_answer)
        # 如果协议没勾选，才点击勾选
        if not self.is_selected(self.agree):
            self.click(self.agree)
        # 点击登录按钮
        self.click(self.submit)

from selenium.webdriver.common.by import By
from util_tools.basePage import BasePage
from time import sleep


class LabelPage(BasePage):
    """点击后打开新的标签页，然后在新的标签页上继续操作"""
    url = "https://leafground.com/window.xhtml"
    # 点击按钮
    click_button = (By.XPATH, '//*[@id="j_idt88:new"]/span')
    # 新的标签页，邮箱输入框
    email_input = (By.ID, 'email')
    # 内容输入框
    message_input = (By.ID, 'message')
    # 新标签页url
    new_page_url = 'https://leafground.com/dashboard.xhtml'

    def open_new_table_operate(self):
        """点击按钮"""
        self.open_url(self.url)
        self.attach_text(self.url, '打开页面网址')
        # 点击之前，记录已有的窗口句柄
        old_windows = set(self.driver.window_handles)
        self.click(self.click_button)
        # 等待并切换到新标签页
        if not self.switch_to_new_tab(old_windows):
            raise RuntimeError("新标签页打开失败，终止后续操作")
        self.attach_text(self.new_page_url, '打开新的标签页网址')
        # 输入邮箱操作
        self.send_keys(self.email_input, 'lisi@163.com')
        # 输入内容操作
        self.send_keys(self.message_input, '这是内容')
        # self.attach_screenshot('输入数据截图')

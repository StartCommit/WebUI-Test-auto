from selenium.webdriver.common.by import By
from util_tools.basePage import BasePage


class FileUploadPage(BasePage):
    """文件上传"""
    url = "https://leafground.com/file.xhtml"
    # 文件选择框
    file_input = (By.XPATH, '//*[@id="j_idt88:j_idt89_input"]')
    # 断言结果
    assert_result = (By.XPATH, '//*[@id="j_idt88:j_idt89"]/span[2]')

    def file_upload(self, file_path='D:/Test/WEB/util_tools/basePage.py'):
        self.open_url(self.url)
        self.attach_text(self.url, '测试页面网址')
        self.attach_text(file_path, '上传文件路径')
        # 上传文件
        self.send_keys(self.file_input, file_path)

    def file_no_upload(self):
        self.open_url(self.url)
        self.attach_text(self.url, '测试页面网址')

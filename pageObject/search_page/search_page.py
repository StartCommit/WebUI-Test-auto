import allure
from selenium.webdriver.common.by import By
from util_tools.basePage import BasePage
from time import sleep


class SearchPage(BasePage):
    url = "/search.php"
    # 高级搜索按钮
    advanced_search = (By.LINK_TEXT, '高级搜索')
    # 关键词搜索框
    search_box = (By.ID, 'keywords')
    # 搜索按钮
    search_button = (By.NAME, 'Submit')
    # 购买
    buy_button = (By.LINK_TEXT, '购买')

    # 添加购物车
    @allure.step("搜索商品并加入购物车")
    def add_to_cart(self):
        """打卡网页"""
        self.open_url(self.url)
        self.attach_text(self.url, '搜索页面网址')
        """点击高级搜索"""
        self.click(self.advanced_search)
        # self.attach_screenshot('高级搜索截图')
        """输入关键词"""
        self.send_keys(self.search_box, '小米')
        """点击搜索"""
        self.click(self.search_button)
        # self.attach_screenshot('搜索结果截图')
        sleep(3)
        """点击购买"""
        self.click(self.buy_button)
        # self.attach_screenshot('购买商品截图')

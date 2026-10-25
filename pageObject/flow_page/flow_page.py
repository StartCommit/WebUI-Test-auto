import allure
from selenium.webdriver.common.by import By
from util_tools.basePage import BasePage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 购物车页面
class FlowPage(BasePage):
    # url
    url = "/flow.php"
    # 商品分类
    category = (By.PARTIAL_LINK_TEXT, '数码产品')
    # # 商品
    product = (By.XPATH, '//*[@alt="小米手机"]')
    # 添加购物车
    add_button = (By.XPATH, '//*[@id="ECS_FORMBUY"]/ul/li[8]/a[1]/img')
    # 结算中心按钮
    settle_button = (By.XPATH, '//*[@alt="checkout"]')
    # 继续购物
    continue_button = (By.XPATH, '//*[@alt="continue"]')
    # 清空购物车
    clear_button = (By.PARTIAL_LINK_TEXT, '清空购物车')
    # 更新购物车
    delete_button = (By.XPATH, '更新购物车')
    # 用户名
    username = (By.NAME, "username")
    # 密码
    password = (By.NAME, "password")
    # 登录
    login_button = (By.NAME, 'login')
    # 不登录，直接配送
    no_login_button = (By.XPATH, '//input[@value="不打算登录，直接购买"]')
    # 注册
    register_button = (By.NAME, 'register')

    # 收货人信息-配送区域
    country = (By.NAME, 'country')
    province = (By.NAME, 'province')
    city = (By.NAME, 'city')
    district = (By.NAME, 'district')

    # 收货人姓名
    consignee = (By.NAME, 'consignee')
    # 收货人地址
    address = (By.NAME, 'address')
    # 电子邮件地址
    email = (By.NAME, 'email')
    # # 手机号码
    phone = (By.NAME, 'tel')
    # 配送按钮
    submit = (By.XPATH, '//input[@value="配送至这个地址"]')
    # 配送方式
    shipping_way = (By.NAME, 'shipping')
    # 支付方式
    payment_way = (By.NAME, 'payment')
    # 提交订单
    submit_order = (By.XPATH, '//input[@type="image"]')

    # 结算购物车操作步骤
    @allure.step("打开购物车，点击结算中心（无商品）")
    def flow_failed(self):
        # 点击结算中心，没有商品的情况
        self.open_url(self.url)
        self.attach_text(self.url, '打开购物车页面')
        self.click(self.settle_button)

    @allure.step("填写收货人信息并提交")
    def _fill_consignee_info(self):
        """填写收货人信息并提交"""
        self.select_by_text(self.country, '中国')
        self.select_by_text(self.province, '北京')
        self.select_by_text(self.city, '北京')
        self.select_by_text(self.district, '东城区')
        self.send_keys(self.consignee, '张三')
        self.send_keys(self.address, '北京市东城区东直门')
        self.send_keys(self.email, '13888888888@163.com')
        self.send_keys(self.phone, '13888888888')
        self.click(self.submit)

    @allure.step("选择配送方式、支付方式、提交订单")
    def _settle(self):
        """选配送方式、支付方式、提交订单"""
        self.click(self.shipping_way)
        self.click(self.payment_way)
        self.click(self.submit_order)
        self.wait_for_url('step=done')


    @allure.step("购物车结算流程")
    def flow_success(self):
        """购物车结算流程"""
        self.open_url(self.url)
        self.attach_text(self.url, '打开购物车页面')
        self.click(self.settle_button)
        # 先判断按钮“不打算登录，直接购买”是否存在
        if self.is_element_present(self.no_login_button):
            # 按钮存在，点击
            self.click(self.no_login_button)
            # 判断有无信息
            if self.is_element_present(self.country):
                self._fill_consignee_info()
                # 无收货人信息 →  填信息 → 结算
                self._settle()
            else:
                # 有收货人信息 →直接结算
                self._settle()
        else:  # 按钮不存在
            if self.is_element_present(self.country):
                self._fill_consignee_info()
                # 无收货人信息 →  填信息 → 结算
                self._settle()
            else:
                # 有收货人信息 →直接结算
                self._settle()
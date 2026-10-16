from pageObject.flow_page.flow_page import FlowPage
from pageObject.search_page.search_page import SearchPage
from time import sleep
import allure


@allure.feature("购物车结算模块")
class TestFlow:
    @allure.story('购物车结算为空流程')
    @allure.title('结算为空流程')
    def test_flow_failed(self, login_driver):
        """测试购物车结算异常流程"""
        flow_page = FlowPage(login_driver)
        flow_page.flow_failed()
        assert flow_page.current_url == 'http://localhost/ecshop/flow.php?step=checkout'
        sleep(3)

    @allure.story('购物车结算正常流程')
    @allure.title('结算正常流程')
    def test_flow_success(self, login_driver):
        """测试购物车结算正常流程"""
        """先将商品加入购物车"""
        SearchPage(login_driver).add_to_cart()
        """进入购物车结算页面"""
        flow_page = FlowPage(login_driver)
        flow_page.flow_success()
        assert flow_page.current_url == 'http://localhost/ecshop/flow.php?step=done'
        sleep(3)

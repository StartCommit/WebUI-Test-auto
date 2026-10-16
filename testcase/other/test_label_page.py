from pageObject.other.label_page import LabelPage
import allure


@allure.feature("打开新标签操作")
class TestLabelPage:
    @allure.story('打开新标签页')
    @allure.title('打开新标签页-进行输入操作')
    def test_label_page(self, not_login_driver):
        label_page = LabelPage(not_login_driver)
        label_page.open_new_table_operate()
        # 断言输入框是否有数据输入
        label_page.assert_element_value_not_empty(label_page.message_input)
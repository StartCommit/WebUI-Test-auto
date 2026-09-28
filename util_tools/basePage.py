import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from config import setting
from util_tools.logs_util.recordlog import logs
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pytesseract
from PIL import Image
from selenium.webdriver.support.ui import Select


class BasePage(object):
    """
    封装浏览器的一些操作，对象webdriver里面的一些方法进行二次开发
    此类封装所有的操作，所有页面继承该类
    """

    def __init__(self, driver):
        # 浏览器对象初始化
        self.__driver = driver
        # 显示等待初始化
        self.__wait = WebDriverWait(self.__driver, setting.WAIT_TIME)

    def window_max(self):
        """浏览器窗口最大化"""
        self.__driver.maximize_window()

    def windows_full(self):
        """浏览器全屏"""
        self.__driver.fullscreen_window()

    def screenshot(self):
        """截图"""
        self.__driver.get_screenshot_as_png()

    def open_url(self, url):
        """打开指定url"""
        self.__driver.get(url)

    @property
    def current_url(self):
        """获取当前页面的url"""
        return self.__driver.current_url

    @property
    def title(self):
        """获取当前页面的标题"""
        return self.__driver.title

    def refresh(self):
        """刷新当前页面"""
        self.__driver.refresh()

    @property
    def switch_to(self):
        """切换switch_to"""
        return self.__driver.switch_to

    def iframe(self, frame):
        """切换iframe内联框架"""
        self.switch_to.frame(frame)

    def exit_iframe(self):
        """退出iframe内联框架"""
        self.switch_to.default_content()

    @property
    def alert(self):
        """切换alert弹窗处理"""
        # return self.switch_to.alert
        return self.__wait.until(ec.alert_is_present())  # 等待alert弹窗出现,存在就返回Alert对象，不存在就返回False

    def alert_confirm(self):
        """alert弹窗点击确定操作"""
        self.alert.accept()

    def alert_cancel(self):
        """alert弹窗点击取消操作"""
        self.alert.dismiss()

    def location_element(self, by, value):
        """
        二次封装find_element方法，定位页面元素
        :param by ：定位方式，比如By.ID,By.XPATH
        :param value:定位表达式
        :return
        """
        try:
            element = self.__wait.until(ec.presence_of_element_located((by, value)))
            logs.info(f"找到元素：{by}={value}")
            return element
        except Exception as e:
            logs.error(f"未找到元素：{by}={value}")
            raise e

    def location_elements(self, by, value):
        """
        二次封装find_elements方法，定位页面元素列表
        :param by ：定位方式，比如By.ID,By.XPATH
        :param value:定位表达式
        :return
        """
        try:
            self.__wait.until(ec.presence_of_all_elements_located((by, value)))
            elements = self.__driver.find_elements(by, value)
            logs.info(f"找到元素列表：{by}={value}")
            return elements
        except Exception as e:
            logs.error(f"未找到元素列表：{by}={value}")
            raise e

    def click(self, locator: tuple, force=False):
        """
        封装点击操作
        :param locator: （tuple）元素定位信息.等于（By.ID,'j_idt88:j_idt93'）
        :param force: 可选参数，强制点击，默认为False
        :return:
        """
        try:
            element = self.location_element(*locator)
            if not force:
                self.__driver.execute_script("arguments[0].click();", element)
            else:
                self.__driver.execute_script(
                    "arguments[0].click({force:true});", element
                )
            logs.info(f"元素点击：{locator}")
        except NoSuchElementException as e:
            logs.error(f"元素定位失败：{locator}")
            raise e

    def send_keys(self, locator: tuple, data):
        """
        封装输入操作,对send_keys方法进行二次封装
        :param locator: 元素定位信息.等于（By.ID,'j_idt88:j_idt93'）
        :param data: 输入的数据
        :return:
        """
        try:
            element = self.location_element(*locator)
            element.send_keys(data)
            logs.info(f"元素被输入内容：{locator},输入的内容是：{data}")
        except NoSuchElementException as e:
            logs.error(f"元素定位失败：{e}")
            raise e

    def enter(self):
        """模拟回车键"""
        try:
            ActionChains(self.__driver).send_keys(Keys.ENTER).perform()
            logs.info(f"按下回车键")
        except Exception as e:
            logs.error(f"输入回车键失败：{e}")
            raise e

    def right_click(self, locator: tuple):
        """
        封装右键点击操作
        :param:locator : tuple定位页面元素
        :return:
        """
        try:
            element = self.location_element(*locator)
            ActionChains(self.__driver).context_click(element).perform()
            logs.info(f"执行右键点击操作：{locator}")
        except NoSuchElementException as e:
            logs.error(f"右键点击失败：{e}")
            raise e

    def double_click(self, locator: tuple):
        """
        封装双击操作
        :param locator: tuple定位页面元素
        :return:
        """
        try:
            element = self.location_element(*locator)
            ActionChains(self.__driver).double_click(element).perform()
            logs.info(f"执行双击操作：{locator}")
        except NoSuchElementException as e:
            logs.error(f"双击失败：{e}")
            raise e

    def screenshots(self, image_name):
        """
        封装截图操作
        :param image_name:文件名
        :return:
        """
        try:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")  # 当前时间
            file_name = f"{image_name}-{current_time}.png"
            file_path = os.path.join(setting.FILE_PATH["screenshot"], file_name)
            self.__driver.get_screenshot_as_file(file_path)
            logs.info(f"截图成功,文件位置：{file_path}")
        except Exception as e:
            logs.error(f"截图失败：{e}")
            raise e

    def clear(self, locator: tuple):
        """
        封装清空操作
        :param locator: 定位元素位置
        :return:
        """
        try:
            element = self.location_element(*locator)
            element.clear()
            logs.info("清空文本")
        except NoSuchElementException as e:
            logs.error(f"双击失败：{e}")
            raise e

    def ocr_capture(self, locator: tuple):
        """
        封装OCR识别操作
        1)定位到图形验证码，保存图片
        2)调用OCR打开图片，识别验证码内容
        :param locator: 定位元素方法和定位表达式
        :return:
        """
        captcha_element = self.location_element(*locator)
        # 截取验证码图片
        captch_path = setting.FILE_PATH["screenshot"] + "/captcha.png"
        captcha_element.screenshot(captch_path)
        # 调用image去打开图像
        captcha_image = Image.open(captch_path)
        try:
            # 调用pytesseract进行ocr识别
            captcha_text = pytesseract.image_to_string(captcha_image)
            logs.info(f"OCR识别成功：{locator},识别结果是：{captcha_text}")
            return captcha_text
        except pytesseract.pytesseract.TesseractNotFoundError:
            logs.error(
                f"找不到tesseract,因为pytesseracts依赖tesseract-ocr引擎进行图像识别！"
            )

    def select_by_index(self, locator: tuple, index: int):
        """通过索引选择下拉框选项"""
        try:
            element = self.location_element(*locator)
            Select(element).select_by_index(index)
            logs.info(f"下拉框选择（索引）：{locator} -> {index}")
        except Exception as e:
            logs.error(f"下拉框选择失败：{locator} -> {index}")
            raise e

    def select_by_value(self, locator: tuple, value: str):
        """通过 value 属性选择下拉框选项"""
        try:
            element = self.location_element(*locator)
            Select(element).select_by_value(value)
            logs.info(f"下拉框选择（value）：{locator} -> {value}")
        except Exception as e:
            logs.error(f"下拉框选择失败：{locator} -> {value}")
            raise e

    def select_by_text(self, locator: tuple, text: str):
        """通过可见文本选择下拉框选项"""
        try:
            element = self.location_element(*locator)
            Select(element).select_by_visible_text(text)
            logs.info(f"下拉框选择（文本）：{locator} -> {text}")
        except Exception as e:
            logs.error(f"下拉框选择失败：{locator} -> {text}")
            raise e

    def deselect_by_index(self, locator: tuple, index: int):
        """通过索引取消选择（多选下拉框）"""
        try:
            element = self.location_element(*locator)
            Select(element).deselect_by_index(index)
            logs.info(f"下拉框取消选择（索引）：{locator} -> {index}")
        except Exception as e:
            logs.error(f"下拉框取消选择失败：{locator} -> {index}")
            raise e

    def deselect_by_value(self, locator: tuple, value: str):
        """通过 value 属性取消选择（多选下拉框）"""
        try:
            element = self.location_element(*locator)
            Select(element).deselect_by_value(value)
            logs.info(f"下拉框取消选择（value）：{locator} -> {value}")
        except Exception as e:
            logs.error(f"下拉框取消选择失败：{locator} -> {value}")
            raise e

    def deselect_by_text(self, locator: tuple, text: str):
        """通过可见文本取消选择（多选下拉框）"""
        try:
            element = self.location_element(*locator)
            Select(element).deselect_by_visible_text(text)
            logs.info(f"下拉框取消选择（文本）：{locator} -> {text}")
        except Exception as e:
            logs.error(f"下拉框取消选择失败：{locator} -> {text}")
            raise e

    def deselect_all(self, locator: tuple):
        """取消所有选项（多选下拉框）"""
        try:
            element = self.location_element(*locator)
            Select(element).deselect_all()
            logs.info(f"下拉框取消所有选择：{locator}")
        except Exception as e:
            logs.error(f"下拉框取消所有选择失败：{locator}")
            raise e

    def is_selected(self, locator: tuple) -> bool:
        """判断元素是否已勾选（用于 checkbox / radio）"""
        element = self.location_element(*locator)
        return element.is_selected()

    def assert_is_element_present(self, locator: tuple):
        """
        判断元素存在，可见
        :param locator: 定位元素方法及定位表达式
        :return:
        """
        try:
            element = self.__driver.find_element(*locator)
            assert element.is_displayed(), '元素不存在'
            return element
        except NoSuchElementException as e:
            logs.error(f"{locator}元素未找到")
            raise AssertionError('元素不存在')

    def assert_element_not_visible(self, locator: tuple):
        """
        判断元素是不存在，不可见
        :param locator: 定位元素方法及定位
        :return:
        """
        try:
            self.__wait.until(ec.invisibility_of_element_located(locator))
        except TimeoutException:
            logs.error("元素可见")

    def assert_title(self, expected_title):
        """
        断言预期标题文本是否包含在实际文本中
        :param expected_title:
        :return:
        """
        assert expected_title in self.__driver.title, '标题不匹配'


if __name__ == "__main__":
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(
        service=Service(r"D:\chromedriver-win64\chromedriver.exe"),
        options=options,
    )
    base = BasePage(driver)

    base.open_url('http://localhost/ecshop/admin/privilege.php?act=login')
    locator = (By.XPATH, '/html/body/form/table/tbody/tr/td[2]/table/tbody/tr[4]/td/img')
    base.ocr_capture(locator)

    # base.open_url('https://leafground.com/input.xhtml')
    # locator = (By.ID, 'j_idt88:name')
    # base.send_keys(locator, '输入内容定位')

    # base.open_url('https://leafground.com/list.xhtml')
    # locator = (By.XPATH, '//*[@id="j_idt88_content"]/div')
    # eles = base.location_elements(By.XPATH, '//*[@id="j_idt88_content"]/div')
    # for i in eles:
    #     i.click()
    #     sleep(1)

    # base.open_url('https://leafground.com/alert.xhtml')
    # # driver.find_element(By.XPATH, '//*[@id="j_idt88:j_idt93"]/span[2]').click()
    # sleep(2)

    # # base.location_element(By.XPATH, '//*[@id="j_idt88:j_idt93"]/span[2]').click()
    # locator = (By.XPATH, '//*[@id="j_idt88:j_idt93"]/span[2]')
    # base.click(locator)

    # base.open_url("https://leafground.com/input.xhtml")
    # local = (By.ID, "j_idt88:j_idt101")
    # base.send_keys(local, "第一行")
    # base.enter()
    # base.send_keys(local, "第二行")
    # base.clear(local)
    # base.right_click(local)
    # base.screenshots("多行文本")

    sleep(3)

import os
import sys
from pathlib import Path
import allure
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from config import setting
from util_tools.logs_util.recordlog import logs
from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException,NoSuchWindowException, NoSuchFrameException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pytesseract
from PIL import Image
from selenium.webdriver.support.ui import Select
from util_tools.handle_data.configParse import ConfigParse


class BasePage(object):
    """
    封装浏览器的一些操作，对象webdriver里面的一些方法进行二次开发
    此类封装所有的操作，所有页面继承该类
    """

    @property
    def driver(self):
        return self.__driver

    def __init__(self, driver):
        # 浏览器对象初始化
        self.__driver = driver
        # 显示等待初始化
        self.__wait = WebDriverWait(self.__driver, setting.WAIT_TIME)
        self.conf = ConfigParse()

    def window_max(self):
        """浏览器窗口最大化"""
        self.__driver.maximize_window()

    def windows_full(self):
        """浏览器全屏"""
        self.__driver.fullscreen_window()

    def screenshot(self):
        """截图"""
        self.__driver.get_screenshot_as_png()

    def refresh(self):
        """刷新当前页面"""
        self.__driver.refresh()

    def scroll_to_button(self):
        """
        使用JavaScript滚动到页面底部
        :return:
        """
        self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    @property
    def current_url(self):
        """获取当前页面的url"""
        return self.__driver.current_url

    @property
    def title(self):
        """获取当前页面的标题"""
        return self.__driver.title

    def open_url(self, url):
        """打开指定url"""
        if url.startswith("http") or url.startswith("https"):
            logs.info(f"打开页面：{url}")
            self.__driver.get(url)
        else:
            new_url = self.conf.get_host('host') + url
            logs.info(f"打开页面：{new_url}")
            self.__driver.get(new_url)

    def get_tag_text(self, locator: tuple):
        """获取标签的文本"""
        try:
            text = self.location_element(*locator).text
            logs.info(f"获取标签的文本内容：{text}")
            return text
        except Exception as e:
            logs.error(f"获取标签的文本失败：{str(e)}")
            return ''

    @property
    def switch_to(self):
        """切换switch_to"""
        return self.__driver.switch_to

    # def iframe(self, frame):
    #     """切换iframe内联框架"""
    #     try:
    #         self.switch_to.frame(frame)
    #         logs.info(f"切换iframe内联框架：{frame}")
    #     except NoSuchFrameException:
    #         logs.error(f"未找到iframe内联框架：{frame}")
    #         raise

    # def switch_to_new_tab(self):
    #     """浏览器打开新的标签页，切换窗口句柄"""
    #     try:
    #         original_windows = self.__driver.window_handles[0]  # 获取当前窗口句柄作为原始窗口
    #         all_window = self.__driver.window_handles  # 获取所有窗口句柄列表
    #         new_window = None
    #         for window in all_window:
    #             if window != original_windows:  # 找到不等于原始窗口句柄的新窗口句柄
    #                 new_window = window
    #                 break
    #         if new_window:
    #             self.__driver.switch_to.window(new_window)  # 切换到新窗口，以便于在新窗口上执行后续操作
    #             logs.info('成功切换到新标签页')
    #         else:
    #             logs.info('没有发现新标签页，继续在当前页面执行')
    #     except Exception as e:
    #         logs.error(f"切换新标签页失败：{e}")

    def switch_to_new_tab(self, old_windows, timeout=5):
        """等待新标签页出现并切换"""
        driver = self.__driver

        try:
            WebDriverWait(driver, timeout).until(
                lambda d: bool(set(d.window_handles) - set(old_windows))
            )

            new_windows = set(driver.window_handles) - set(old_windows)
            new_window = next(iter(new_windows))

            driver.switch_to.window(new_window)
            logs.info(f'成功切换到新标签页：{new_window}')
            return True

        except TimeoutException:
            logs.error(f'等待新标签页超时：{timeout} 秒')
            return False

        except Exception as e:
            logs.error(f'切换新标签页失败：{e}')
            return False

    def switch_to_tab_by_index(self, index):
        """
        通过索引切换新标签页
        :param index: 新标签页的索引,从0开始
        :return:
        """
        try:
            all_window = self.__driver.window_handles
            if 0 <= index < len(all_window):
                self.switch_to.window(all_window[index])
                logs.info(f"成功切换到第{index + 1}个标签页")
            else:
                logs.error(f"指定的窗口索引超出范围：{index}")
        except Exception as e:
            logs.error(f"切换新标签页失败：{str(e)}")

    def iframe(self, locator):
        """切换iframe内联框架，locator 是 (By, value) 元组"""
        try:
            self.__wait.until(EC.frame_to_be_available_and_switch_to_it(locator))
            logs.info(f"切换iframe内联框架：{locator}")
        except Exception:
            logs.error(f"未找到iframe内联框架：{locator}")
            raise

    def exit_iframe(self):
        """退出iframe内联框架"""
        self.switch_to.default_content()

    @property
    def alert(self):
        """切换alert弹窗处理"""
        # return self.switch_to.alert
        return self.__wait.until(EC.alert_is_present())  # 等待alert弹窗出现,存在就返回Alert对象，不存在就返回False

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
            element = self.__wait.until(EC.presence_of_element_located((by, value)))
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
            self.__wait.until(EC.presence_of_all_elements_located((by, value)))
            elements = self.__driver.find_elements(by, value)
            logs.info(f"找到元素列表：{by}={value}")
            return elements
        except Exception as e:
            logs.error(f"未找到元素列表：{by}={value}")
            raise e

    def visibility_of_element_located(self, by, value):
        """
        等待元素可见性
        :param by:
        :param value:
        :return:
        """
        try:
            element = self.__wait.until(EC.visibility_of_element_located((by, value)))
            logs.info(f"找到元素：{by} = {value}")
            return element
        except Exception as e:
            logs.error(f"在设定时间内未找到元素：{by} = {value}")
            raise e

    def click(self, locator: tuple, force=False):
        """
        封装点击操作
        """
        try:
            element = self.location_element(*locator)

            # 如果你手动传了 force，直接用 JS
            if force:
                self.__driver.execute_script("arguments[0].click();", element)
                logs.info(f"元素点击(JS强点)：{locator}")
                return

            # 没传 force，先尝试普通点击
            try:
                element.click()
                logs.info(f"元素点击：{locator}")
            except ElementClickInterceptedException:
                # 如果被遮挡了，自动转成 JS 点击，并记录一条警告
                logs.warning(f"元素被遮挡，自动切换为JS点击：{locator}")
                self.__driver.execute_script("arguments[0].click();", element)
                logs.info(f"元素点击(JS兜底)：{locator}")

        except NoSuchElementException as e:
            logs.error(f"元素定位失败：{locator}")
            raise e

    def click_actions(self, locator: tuple):
        """
        封装模拟鼠标点击操作
        :param locator: （tuple）定位元素信息，等于(By.ID,'j_idt88:j_idt93')
        :return:
        """
        element = self.visibility_of_element_located(*locator)
        ActionChains(self.__driver).click(element).perform()

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

    def send_keys_actions(self, locator: tuple, data):
        """
        模拟键盘的输入操作
        :param locator: （tuple）元素定位信息.等于（By.ID,'j_idt88:j_idt93'）
        :param data: 输入的数据
        :return:
        """
        try:
            element = self.location_element(*locator)
            ActionChains(self.__driver).move_to_element(element).click().send_keys(data).perform()
            logs.info(f"元素被输入内容：{locator},输入的内容是：{data}")
            return element
        except NoSuchElementException as e:
            logs.error(f"元素定位失败：{e}")
            raise e

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

    def mouse_hover_actions(self, locator: tuple):
        """
        封装鼠标悬停展示内容或弹框
        :param locator: （tuple）定位页面元素
        :return:
        """
        try:
            move_element = self.location_element(*locator)
            ActionChains(self.__driver).move_to_element(move_element).perform()
            logs.info('鼠标悬停')
        except Exception as e:
            logs.error(f"鼠标悬停出现异常：{e}")
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
            return file_path
        except Exception as e:
            logs.error(f"截图失败：{e}")
            raise e

    def screenshots_png(self):
        """
        页面截屏，保存为png文件
        :return:
        """
        return self.__driver.get_screenshot_as_png()

    def attach_screenshot(self, name='截图', attachment_type=allure.attachment_type.PNG):
        """
        把当前页面截图附加到 allure 报告
        :param name: 附件在报告里的显示名字
        :param attachment_type: 附件类型，默认 PNG
        """
        try:
            png = self.screenshots_png()
            allure.attach(png, name=name, attachment_type=attachment_type)
            logs.info(f'allure 附件已添加：{name}')
        except Exception as e:
            logs.error(f'添加 allure 截图附件失败：{e}')
            raise e

    def attach_file(self, file_path, name='附件', attachment_type=allure.attachment_type.TEXT):
        """
        把指定文件作为附件附加到 allure 报告
        :param file_path: 文件路径
        :param name: 附件显示名字
        :param attachment_type: 附件类型
        """
        try:
            allure.attach.file(file_path, name=name, attachment_type=attachment_type)
            logs.info(f'allure 文件附件已添加：{name} -> {file_path}')
        except Exception as e:
            logs.error(f'添加 allure 文件附件失败：{e}')
            raise e

    def attach_text(self, content, name='文本'):
        """
        把一段文本作为附件附加到 allure 报告
        :param content: 文本内容
        :param name: 附件显示名字
        """
        try:
            allure.attach(content, name=name, attachment_type=allure.attachment_type.TEXT)
            logs.info(f'allure 文本附件已添加：{name}')
        except Exception as e:
            logs.error(f'添加 allure 文本附件失败：{e}')
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
            logs.error(f"清空文本失败：{e}")
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
        captcha_path = setting.FILE_PATH["screenshot"] + "/captcha.png"
        captcha_element.screenshot(captcha_path)
        # 调用image去打开图像
        captcha_image = Image.open(captcha_path)
        try:
            # 调用pytesseract进行ocr识别
            captcha_text = pytesseract.image_to_string(captcha_image)
            logs.info(f"OCR识别成功：{locator},识别结果是：{captcha_text}")
            return captcha_text
        except pytesseract.pytesseract.TesseractNotFoundError:
            logs.error(
                f"找不到tesseract,因为pytesseracts依赖tesseract-ocr引擎进行图像识别！"
            )

    def is_selected(self, locator: tuple) -> bool:
        """判断元素是否已勾选（用于 checkbox / radio）"""
        element = self.location_element(*locator)
        return element.is_selected()

    def is_element_present(self, locator: tuple) -> bool:
        """
        判断元素存在
        :param locator: 定位元素方法及定位表达式
        :return:
        """
        try:
            self.__wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

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
            raise AssertionError(f'元素不存在{e}')

    def assert_element_not_visible(self, locator: tuple):
        """
        判断元素是不存在，不可见
        :param locator: 定位元素方法及定位
        :return:
        """
        try:
            self.__wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            logs.error("元素可见，断言失败")
            raise AssertionError("元素可见")

    def assert_title(self, expected_title):
        """
        断言预期标题文本是否包含在实际文本中
        :param expected_title:
        :return:
        """
        assert expected_title in self.__driver.title, '标题不匹配'

    def assert_element_to_be_clickable(self, locator: tuple):
        """
        断言元素是否可被点击操作
        :param locator: （tuple）元素定位表达式
        :return:
        """
        try:
            element = self.__wait.until(
                EC.element_to_be_clickable(locator)
            )
            # 执行断言或其他操作
            assert element.is_enabled(), "元素未启用交互"
            logs.info('断言结果：元素是可点击的，并且可以进行交互')
            # 例如，点击元素
            element.click()
        except Exception as e:
            logs.error(f"发生错误: {e}")

    # def assert_element_value_not_empty(self, locator: tuple):
    #     """断言输入框内容不为空"""
    #     try:
    #         value = self.location_element(*locator).get_attribute('value')
    #         assert value, f'输入框内容为空：{locator}'
    #         logs.info(f'输入框内容不为空：{value}')
    #     except Exception as e:
    #         logs.error(f'输入框内容断言失败：{e}')
    #         raise

    def get_element_text_content(self, locator: tuple) -> str:
        """
        通用获取元素内容（支持普通输入框 input/textarea 以及 富文本框 div）
        :param locator: 元素定位
        :return: 去除首尾空格后的文本内容
        """
        try:
            element = self.location_element(*locator)
            # 1. 优先尝试获取 value 属性（针对 input, textarea）
            value = element.get_attribute('value')
            if value is not None:
                return str(value).strip()

            # 2. 尝试获取 textContent 属性（针对 div 富文本框）
            text_content = element.get_attribute('textContent')
            if text_content is not None:
                return str(text_content).strip()

            # 3. 兜底使用 text 属性
            return element.text.strip()
        except Exception as e:
            logs.error(f"获取元素内容失败：{e}")
            return ""

    def assert_element_not_empty(self, locator: tuple):
        """
        通用断言：元素内容不为空（支持输入框 input/textarea 和 富文本框 div）
        :param locator: 元素定位
        """
        content = self.get_element_text_content(locator)
        assert content != '', f'元素内容为空，断言失败：{locator}'
        logs.info(f'元素内容不为空，实际内容为：{content}')

    def get_element_value(self, locator: tuple):
        """获取输入框/文本域的内容"""
        try:
            value = self.location_element(*locator).get_attribute('value')
            logs.info(f"获取输入框内容：{value}")
            return value
        except Exception as e:
            logs.error(f"获取输入框内容失败：{str(e)}")
            return ''

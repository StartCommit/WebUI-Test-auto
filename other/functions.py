from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# webdriver初始化
driver = webdriver.Chrome(service=Service(r"D:\chromedriver-win64\chromedriver.exe"))

# 页面导航
driver.get("http://localhost/ecshop/user.php?act=register")
sleep(1)

# 窗口最大化
driver.maximize_window()

# 查找元素
driver.find_element(By.ID, "username")

# 与元素交互，在网页上执行各种操作
driver.find_element(By.ID, "email").send_keys("123456789@163.com")
driver.find_element(By.XPATH, "//input[@name='Submit']").click() # 点击函数

# 下拉框的处理
els = driver.find_element(By.NAME, "sel_question")
sel = Select(els)
sel.select_by_index(3) # 通过下拉框索引值进行选择
sel.select_by_value("favorite_movie") # 通过下拉选项标签的value属性值进行选择
sel.select_by_visible_text("我最大的爱好？") # 通过下拉选项标签的文本内容进行选择
sel.deselect_by_index(2) # 当下拉框选项多选的情况下，通过索引取消选择
sel.deselect_by_value("favorite_movie") # 当下拉框选项多选的情况下，通过标签的value属性取消选择
sel.deselect_by_visible_text("我最大的爱好？") # 当下拉框选项多选的情况下，通过标签的文本内容取消选择
sel.deselect_all() # 取消所有选项

# 警告框的处理
alert = driver.switch_to.alert
sleep(3)
alert.accept()

# 单选按钮
driver.get("https://leafground.com/radio.xhtml")
driver.find_element(By.XPATH, '//*[@id="j_idt87:console1"]/tbody/tr/td[4]/label').click()

# # 滑动条

sleep(2)
# 定位滑块元素
slider = driver.find_element(By.ID, 'j_idt106:j_idt120')

# 获取元素滑块的宽度
slider_width = slider.size['width']

# 计算要拖动的偏移量(比如说要滑动到一半的位置)
offset = slider_width / 5

# 使用ActionChains类进行拖动操作
actions = ActionChains(driver)

# click_and_hold() 点击并保持住滑块元素，准备拖动；move_by_offset() 通过指定的偏移量移动滑块元素；release() 释放滑块元素
actions.click_and_hold(slider).move_by_offset(offset, 0).release().perform()

# 文本框实现自增或自减操作
number_input = driver.find_element(By.ID, "j_idt106:j_idt118_input")
# 清空输入框
number_input.clear()
# 手动输入新的值
number_input.send_keys("10")
# 使用文本框上的向上箭头模拟值自增
number_input.send_keys(Keys.ARROW_UP)
sleep(2)
# 使用文本框上的向下箭头模拟值自减
number_input.send_keys(Keys.ARROW_DOWN)

# 文本框跳出日期选择框处理
date_input = driver.find_element(By.ID,"j_idt106:j_idt116_input")
# 点击触发日期选择框
date_input.click()
# 定位到日期选择框中的元素
driver.find_element(By.XPATH, '//*[@id="j_idt106:j_idt116_panel"]/div/div[2]/table/tbody/tr[4]/td[5]/a').click()

#  页面截图
driver.get_screenshot_as_file("screenshot.png")


sleep(3)

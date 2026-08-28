import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 指定存放 chromedriver.exe 的绝对路径（注意要用双斜杠或者 r 前缀）
driver = webdriver.Chrome(service=Service(r"D:\chromedriver-win64\chromedriver.exe"))
# 切换成edge浏览器
# driver = webdriver.Edge()

# 访问百度界面
driver.get("https://www.baidu.com")

# 元素定位
# driver.find_element_by_id("chat-textarea") # 通过id定位(3.0)
# driver.find_element_by_name("chat-textarea") # 通过name定位
# driver.find_element_by_class_name("chat-input-textarea chat-input-scroll-style") # 通过id定位
els = driver.find_element(By.ID,'chat-textarea').send_keys("selenium4.0新特性") # 通过id定位(4.0)
time.sleep(10) # 留给你看清输入效果

# 打开新的窗口
driver.switch_to.new_window()
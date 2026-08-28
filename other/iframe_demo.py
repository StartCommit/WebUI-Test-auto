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
driver.get("https://leafground.com/frame.xhtml")
sleep(2)

# 根据索引切换到第3个frame框架
driver.switch_to.frame(2)

# 进入内嵌框架
driver.switch_to.frame(0)

# 找到按钮并点击
driver.find_element(By.XPATH,'//*[@id="Click"]').click()

# 切换到父窗口（退出内嵌框架）
driver.switch_to.default_content()

sleep(2)

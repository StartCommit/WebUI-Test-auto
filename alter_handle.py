from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# webdriver初始化
driver = webdriver.Chrome(service=Service(r"D:\chromedriver-win64\chromedriver.exe"))

driver.get("https://leafground.com/alert.xhtml")
driver.maximize_window()
sleep(2)

# alter 警告框处理
driver.find_element(By.XPATH, '//*[@id="j_idt88:j_idt91"]/span[2]').click()
alter = driver.switch_to.alert
sleep(2)
alter.accept()
sleep(2)

# alter (Confirm Dialog) ，有确定和取消按钮的弹框
driver.find_element(By.XPATH, '//*[@id="j_idt88:j_idt93"]/span[2]').click()
alter = driver.switch_to.alert
sleep(2)
# alter.accept() # 点击确定
alter.dismiss() # 点击取消
sleep(2)

# Sweet Alert (Simple Dialog)弹框处理
driver.find_element(By.XPATH, '//*[@id="j_idt88:j_idt95"]/span[2]').click()
sleep(2)
driver.find_element(By.XPATH, '//*[@id="j_idt88:j_idt98"]/span[2]').click()
sleep(2)

# Sweet Modal Dialog 弹框处理
driver.find_element(By.XPATH, '//*[@id="j_idt88:j_idt100"]/span[2]').click()
sleep(2)
driver.find_element(By.XPATH, '//*[@id="j_idt88:j_idt101"]/div[1]/a/span').click()
sleep(2)
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service(r"D:\chromedriver-win64\chromedriver.exe"))

# 打开网页
driver.get("http://localhost/ecshop/user.php?act=register")
# id元素定位
# driver.find_element(By.ID, "username").send_keys("用户名")
# sleep(5)
# name元素定位
# driver.find_element(By.NAME, "email").send_keys("邮箱")
# sleep(5)
# class_name元素定位
# driver.find_element(By.CLASS_NAME, "inputBg")#可能会重复
# sleep(5)
# tag_name元素定位
# driver.find_element(By.TAG_NAME, "input")#可能会重复
# sleep(5)

# css_select选择器元素定位
# 1)id选择器   #+id属性值
# driver.find_element(By.CSS_SELECTOR, "#username")

# 2)类选择器   .+类属性值
# driver.find_element(By.CSS_SELECTOR, ".inputBg")

# 3)标签选择器   标签名  查找第一个<input>标签
# driver.find_element(By.CSS_SELECTOR, "input")

# 4）属性选择器   [属性名="属性值"]
# driver.find_element(By.CSS_SELECTOR, "[name='email']").send_keys("邮箱") # 单个属性定位
# driver.find_element(By.CSS_SELECTOR, "[name='email'][type='text']").send_keys("邮箱")  # 多属性定位
driver.find_element(By.CSS_SELECTOR, "input[name='extend_field1']").send_keys("MSN") # 属性值包含
sleep(3)

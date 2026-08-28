from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep

driver = webdriver.Chrome(service=Service(r"D:\chromedriver-win64\chromedriver.exe"))
driver.maximize_window()
driver.get("https://leafground.com/select.xhtml")

# 强制等待 作用于单个
sleep(5)
driver.find_element(By.ID, 'j_idt87:country_label').click()
sleep(2)

# 显示等待 作用于单个
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "j_idt87:country_label"))
    ).click()
except Exception as e:
    # 先打印报错原因，方便在控制台排查
    print(f"点击元素失败，错误原因: {e}")
    # 保存截图
    driver.get_screenshot_as_file("./image/screenshot.png")


# 隐式等待  作用于全局
driver.implicitly_wait(10)  # 设置隐式等待时间10秒

driver.find_element(By.ID, "j_idt87:country_label").click()
driver.find_element(By.XPATH, 'j_idt87:city_label').click()

sleep(2)
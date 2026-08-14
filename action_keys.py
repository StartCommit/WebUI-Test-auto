from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# webdriver初始化
driver = webdriver.Chrome(service=Service(r"D:\chromedriver-win64\chromedriver.exe"))

driver.get("https://leafground.com/input.xhtml")
driver.maximize_window()
sleep(2)


# 模拟键盘的操作
# 定位到多行文本框元素
line_element = driver.find_element(By.ID, "j_idt88:j_idt101")
line_element.send_keys("多行文本框第一行")
# 模拟键盘回车键
# line_element.send_keys(Keys.ENTER) # 推荐使用
ActionChains(driver).send_keys(Keys.ENTER).perform()
sleep(2)
line_element.send_keys("多行文本框第二行")


# 模拟鼠标的操作
# 1)点击 .click()
driver.find_element(By.ID, "j_idt88:j_idt101").click()

# 2)右键点击 context_click
els = driver.find_element(By.ID, "j_idt88:j_idt101")
ActionChains(driver).context_click(els).perform()

# 3)双击 double_click
double_els = driver.find_element(By.ID, "j_idt88:j_idt91")
ActionChains(driver).double_click(double_els).perform()

# 4)鼠标悬停 move_to_element
hover_els = driver.find_element(By.XPATH, '//*[@id="menuform:j_idt36"]/a/i[1]')
ActionChains(driver).move_to_element(hover_els).perform()

# # 5)拖拽元素 drag_and_drop
drag_els = driver.find_element(By.XPATH, '//*[@id="j_idt106:j_idt120"]/span')
drop_els = driver.find_element(By.XPATH, '//*[@id="j_idt106:j_idt120"]/span')
ActionChains(driver).drag_and_drop(drag_els, drop_els).perform()

# 6)鼠标滚动
ActionChains(driver).move_to_element(100,500).perform()
# 使用JavaScript执行向下滚动
driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

driver.get("https://leafground.com/select.xhtml")
sleep(3)


# 下拉菜单有多个选项，模拟鼠标滚动到最底部那个，点击
dropdown = driver.find_element(By.ID, 'j_idt87:lang_label').click()
# 模拟鼠标向下滚轮
for _ in range(8):
    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()


sleep(4)
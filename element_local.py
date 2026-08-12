from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service(r"D:\chromedriver-win64\chromedriver.exe"))

# 打开网页
driver.get("http://localhost/ecshop/user.php?act=register")
sleep(2)
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

# driver.find_element(By.CSS_SELECTOR, "input[name='extend_field1']").send_keys("MSN") # 通过标签名+属性选择器组合定位

# driver.find_element(By.CSS_SELECTOR, "input#username").send_keys("用户名")  # 标签名+id选择器组合定位

# driver.find_element(By.CSS_SELECTOR, "input.inputBg").send_keys("用户名") # 通过类名+标签名组合定位

# driver.find_element(By.CSS_SELECTOR, "table>tbody>tr:") #通过标签层级定位

# driver.find_element(By.CSS_SELECTOR, "table>tbody>tr:nth-child(2) td:nth-child(2) input[type='text']").send_keys("邮箱") # 表格层级定位

# 5)模糊定位
# driver.find_element(By.CSS_SELECTOR, "a[href*='user.php?act=login']").click()

# link_text元素定位（全部文本）
# driver.find_element(By.LINK_TEXT, "我已有账号，我要登录").click()

# partial_link_text元素定位(部分文本)
# driver.find_element(By.PARTIAL_LINK_TEXT, "登录").click()

# xpath元素定位

# 1）绝对路径:语法：/html/body/div[7]/div/form/table/tbody/tr[1]/td[2]/input /表示根节点
# driver.find_element(By.XPATH, "/html/body/div[7]/div/form/table/tbody/tr[1]/td[2]/input").send_keys("用户名")

# 2）相对路径:语法: //+标签名[@属性名='属性值']
# driver.find_element(By.XPATH, '//input[@id="email"]').send_keys("邮箱")

# 3）通过文本内容定位（精确定位）；语法:使用text()函数定位
# driver.find_element(By.XPATH, '//*[text()="我已有账号，我要登录"]').click()

# 4）通过部分文本内容定位（模糊定位）；语法:使用contains()函数定位
# driver.find_element(By.XPATH, '//*[contains(text(),"登录")]').click()

# 5）通过属性值定位；语法:使用@属性名=属性值
# driver.find_element(By.XPATH, '//input[@name="email"]').send_keys("测试邮箱")

# 6）通过逻辑运算符定位；语法://*[属性名='属性值'] and @属性名='属性值'
# driver.find_element(By.XPATH, '//input[@name="email" and @id="email"]').send_keys("测试邮箱")

# 7）通过函数；语法://input[contains(@class,"inputBg")]
# driver.find_element(By.XPATH, '//input[contains(@class,"inputBg")]').send_keys("测试")
sleep(2)

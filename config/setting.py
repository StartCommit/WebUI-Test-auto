import os
import sys

DIR_PATH: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_PATH)

# 显示等待时间设置。默认10 秒
WAIT_TIME = 10

# 浏览器设置
browser_type = "chrome"

# 驱动器位置
DRIVER_PATH = {
    'chrome': r"D:\chromedriver-win64\chromedriver.exe",
    'edge': r"D:\edgedriver-win64\msedgedriver.exe",
    'firefox': r"D:\geckodriver-win64\geckodriver.exe",
}

# 设置是否发送钉钉群
is_send_ding = True

# 文件路径
FILE_PATH = {
    "config": os.path.join(DIR_PATH, 'config', 'config.ini'),
    "log": os.path.join(DIR_PATH, "log"),
    "report": os.path.join(DIR_PATH, "report"),
    "data": os.path.join(DIR_PATH, "data"),
    "screenshot": os.path.join(DIR_PATH, "screenshot")
}

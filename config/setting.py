import os
import sys

# from util_tools.logs_util.recordlog import logs

DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_PATH)

# 显示等待时间设置。默认10 秒
WAIT_TIME = 10

# 浏览器设置
browser_type = "chrome"

# 文件路径
FILE_PATH = {
    "config": os.path.join(DIR_PATH, "config.ini"),
    "log": os.path.join(DIR_PATH, "log"),
    "report": os.path.join(DIR_PATH, "report"),
    "data": os.path.join(DIR_PATH, "data"),
    "screenshot": os.path.join(DIR_PATH, "screenshot")
}
# logs.info(FILE_PATH) 只能在util_tools下创建一个重新引用logs使用

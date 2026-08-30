import os
import sys
# from util_tools.logs_util.recordlog import logs

DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_PATH)

# 文件路径
FILE_PATH = {
    "config": os.path.join(DIR_PATH, "config.ini"),
    "log": os.path.join(DIR_PATH, "log"),
    "report": os.path.join(DIR_PATH, "report"),
    "data": os.path.join(DIR_PATH, "data")
}
# logs.info(FILE_PATH) 只能在util_tools下创建一个重新引用logs使用
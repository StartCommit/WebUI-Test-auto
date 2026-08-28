import os
import sys

DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_PATH)

# 文件路径
FILE_PATH = {
    "config": os.path.join(DIR_PATH, "config.ini"),
    "log": os.path.join(DIR_PATH, "log"),
    "report": os.path.join(DIR_PATH, "report"),
    "data": os.path.join(DIR_PATH, "data")
}
print(FILE_PATH['log'])
import os
import json
from config.setting import FILE_PATH


def read_json(file_path):
    """
    读取json文件
    :param file_path: 支持文件名（如 'login_success.json'）或绝对路径
    :return: 返回列表类型，列表中每个元素为元组数据，如：[("admin", "admin1314"), ("admin", "admin1314")]
    """
    try:
        # 不是绝对路径，就拼到 data 目录下
        if not os.path.isabs(file_path):
            file_path = os.path.join(FILE_PATH['data'], file_path)

        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
            data_list_tuple = [tuple(data_dict.values()) for data_dict in data]
            return data_list_tuple
    except Exception as e:
        print('读取json文件数据异常,异常原因为{}'.format(e))

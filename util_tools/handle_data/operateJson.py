import json


def read_json(file_path):
    """
    读取json文件
    :param file_path: 文件路径
    :return:返回列表类型，列表中每个元素为元组数据，如：[("lisi", "dongli1314"), ("lisi", "dongli1314")]
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
            data_list_tuple = [tuple(data_dict.values()) for data_dict in data]
            return data_list_tuple
    except Exception as e:
        print('读取json文件数据异常,异常原因为{}'.format(e))

# res = read_json('../../data/login.json')
# print(res)

import yaml
from util_tools.logs_util.recordlog import logs
def read_yaml(file_path):
    """
    读取yaml文件的数据
    :param file_path: yaml文件路径
    :return: 返回列表类型，列表中每个元素为元组数据，如：[("lisi", "dongli1314"), ("lisi", "dongli1314")]
    """
    try:
        data_list_tuple = []
        with open(file_path, encoding="utf-8") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            for data_str in data:
                if data_str is not None:
                    data_tuple = tuple(data_str.split(','))
                    data_list_tuple.append(data_tuple)
            return data_list_tuple
    except Exception as e:
        logs.error('读取yaml文件数据异常，异常原因为{}'.format(e))

res = read_yaml('D:/Test/WEB/data/login.yaml')
print(res)
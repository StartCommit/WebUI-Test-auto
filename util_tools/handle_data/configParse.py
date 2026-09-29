import configparser
from config.setting import FILE_PATH
from util_tools.logs_util.recordlog import logs


class ConfigParse:
    """
    解析.ini配置文件解析
    """

    def __init__(self, file_path=FILE_PATH['config']):
        self.config = configparser.ConfigParser()
        self.file_path = file_path
        self.read_config()

    def read_config(self):
        """
        读取配置文件
        :return:
        """
        try:
            self.config.read(self.file_path, encoding="utf-8")
        except Exception as e:
            logs.error("读取配置文件失败：{}".format(e))

    def get_value(self, section, option):
        """
        获取配置文件值
        :param section:
        :param option:
        :return:
        """
        try:
            value = self.config.get(section, option)
            # logs.info("获取配置文件值成功：{}".format(value))
            return value
        except Exception as e:
            logs.error(f'获取配置文件值失败,原因是：{e}')

    def get_host(self, option):
        """
        获取host
        :return:
        """
        host = self.get_value('HOST', option)
        return host


if __name__ == '__main__':
    config = ConfigParse()
    # res = config.get_value('HOST', 'host')
    res = config.get_host('host')
    print(res)

# -*- coding: utf-8 -*-
import logging
import os
import time
import colorlog

from logging.handlers import RotatingFileHandler #按文件大小滚动备份
from config import setting

log_path = setting.FILE_PATH['log']
if not os.path.exists(log_path):
    os.mkdir(log_path)

logfile_name = log_path + r"\test.{}.log".format(time.strftime("%Y%m%d"))

class RecordLog():
    def __init__(self):
        pass

    @classmethod
    def log_color(cls):
        log_color_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING':'yellow',
            'ERROR':'red',
            'CRITICAL':'red'
            }
        formater = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s',
            log_colors=log_color_config)# 传入颜色映射
        return formater

    def output_logging(self):
        logger = logging.getLogger(__name__)
        stream_format = self.log_color()
        # 防止重复打印日志
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s'
            )
            # 把log日志信息输出打破控制台
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(stream_format)
            logger.addHandler(sh)

            # 把log日志信息输出到指定文件中
            fh = RotatingFileHandler(filename=logfile_name,mode='a',maxBytes=5242880,backupCount=7,encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(log_format)
            logger.addHandler(fh)

        return logger

rec = RecordLog()
logs = rec.output_logging()

# logs.info("这是info级别日志")
# logs.error("这是error级别日志")
# logs.warning("这是warning级别日志")
# logs.debug("这是debug级别日志")
# logs.critical("这是critical级别日志")

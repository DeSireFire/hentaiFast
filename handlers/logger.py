#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2020/12/19 
# CreatTIME : 22:31 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire

__author__ = 'RaXianch'

from handlers import *
import logging
from logging.handlers import TimedRotatingFileHandler
'''
日志logger类
'''

# 创建logs文件夹
# cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path = BASE_DIR
log_path = os.path.join(cur_path, 'logs')
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path): os.mkdir(log_path)


class Log(object):
    def __init__(self):
        # 文件的命名
        self.logname = os.path.join(log_path, '%s.log' % time.strftime('%Y_%m_%d'))
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        # 日志输出格式
        # self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')
        self.formatter = logging.Formatter(
            "[%(asctime)s] [%(process)d] [%(levelname)s] "
            "- %(module)s.%(funcName)s (%(filename)s:%(lineno)d) "
            "- %(message)s"
        )

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        # fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')  # 这个是python3的
        # interval 滚动周期，
        # when="MIDNIGHT", interval=1 表示每天0点为更新点，每天生成一个文件
        # backupCount  表示日志保存个数
        fh = TimedRotatingFileHandler(
            filename=self.logname, when="MIDNIGHT", interval=1, backupCount=30
        )
        # filename="mylog" suffix设置，会生成文件名为mylog.2020-02-25.log
        fh.suffix = "%Y-%m-%d.log"
        # extMatch是编译好正则表达式，用于匹配日志文件名后缀
        # 需要注意的是suffix和extMatch一定要匹配的上，如果不匹配，过期日志不会被删除。
        fh.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        # 定义日志输出格式
        fh.setLevel(logging.INFO)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)




if __name__ == '__main__':
    pass
    logger = Log()

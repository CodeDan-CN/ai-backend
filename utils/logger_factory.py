import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler
from config.setting import LOG_CONFIG


class LoggerSingleton:
    _instance = None

    def __new__(cls, name):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance._init_logger(name)
        return cls._instance

    def _init_logger(self, name):
        # 创建日志目录
        log_dir = LOG_CONFIG["url"]
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 定义日志文件的基本名称（没有后缀）
        log_file_base = os.path.join(log_dir, LOG_CONFIG["name"])

        # 配置 TimedRotatingFileHandler
        handler = TimedRotatingFileHandler(
            log_file_base, when="MIDNIGHT", interval=1, backupCount=7, encoding='utf-8'
        )

        time_format = LOG_CONFIG["time_format"]
        handler.suffix = f"{time_format}.log"  # 文件名后缀，按分钟进行轮换

        # 修改 extMatch 以匹配文件名格式
        handler.extMatch = re.compile(r"^\d{4}\d{2}\d{2}.log$")  # 匹配日期和时间格式的文件名

        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # 创建日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

        # 配置 StreamHandler（控制台日志处理器）
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # 添加控制台处理器
        self.logger.addHandler(console_handler)

        # 设置日志记录器的级别
        self.logger.setLevel(logging.DEBUG)

    def get_logger(self):
        return self.logger


def get_logger(name):
    return LoggerSingleton(name).get_logger()


logger = get_logger('ai-backend')

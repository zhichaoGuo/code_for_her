import logging
import os


class LogUtils:
    _instance = None

    def __new__(cls, log_file_path="."):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.logger = logging.getLogger("query_poi")
            cls._instance.logger.setLevel(logging.DEBUG)

            if not cls._instance.logger.hasHandlers():
                file_handler = logging.FileHandler(os.path.join(log_file_path, "query_poi.log"), encoding='utf-8')
                file_handler.setLevel(logging.DEBUG)

                formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
                file_handler.setFormatter(formatter)

                cls._instance.logger.addHandler(file_handler)
        return cls._instance

    def get_logger(self):
        return self.logger

my_logger = LogUtils().get_logger()
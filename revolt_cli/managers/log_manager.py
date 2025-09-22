import os
import logging
from logging.handlers import RotatingFileHandler


class LogManager:
    def __init__(self, name, log_file, log_level=logging.INFO):
        self.log_file = log_file
        self.log_level = log_level

        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)

        file_handler = RotatingFileHandler(self.log_file, maxBytes=1024*1024*5, backupCount=5)
        file_handler.setLevel(self.log_level)

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
# util
import logging
import logging.handlers
from os import path
import os


# http://ourcstory.tistory.com/97
# http://ourcstory.tistory.com/105
# TODO change to singleton
# TODO more comment
class Logger(object):
    LOG_FOLDER_NAME = 'log'
    LOG_PATH = path.join('.', LOG_FOLDER_NAME)

    LOG_FORMAT = '[%(levelname)s | %(filename)s:%(lineno)s] %(asctime)s > %(message)s'

    def __init__(self, logger_name):
        self.log = logging.getLogger(logger_name)
        self.log.setLevel(logging.DEBUG)

        # make dir for log path
        if not path.exists(self.LOG_PATH):
            os.makedirs(self.LOG_PATH)

        self.LOG_FULL_PATH = path.join(self.LOG_PATH, self.LOG_FOLDER_NAME)

        formatter = logging.Formatter(self.LOG_FORMAT)

        # add file handler
        self.file_handler = logging.FileHandler(self.LOG_FULL_PATH)
        self.file_handler.setFormatter(formatter)
        self.log.addHandler(self.file_handler)

        # add stdout handler
        # self.stream_handler = logging.StreamHandler()
        # self.stream_handler.setFormatter(formatter)
        # self.log.addHandler(self.stream_handler)


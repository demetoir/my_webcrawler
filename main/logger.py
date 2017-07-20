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

    def __init__(self, logger_name):
        self.log = logging.getLogger(logger_name)
        self.log.setLevel(logging.DEBUG)

        # make dir for log path
        if not path.exists(self.LOG_PATH):
            os.makedirs(self.LOG_PATH)

        self.LOG_FOLDER_NAME = logger_name + '.log'
        self.LOG_FULL_PATH = path.join(self.LOG_PATH, self.LOG_FOLDER_NAME)

        formatter = logging.Formatter('[%(levelname)s | %(filename)s:%(lineno)s] %(asctime)s > %(message)s')

        file_handler = logging.FileHandler(self.LOG_FULL_PATH)
        stream_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self.log.addHandler(file_handler)
        self.log.addHandler(stream_handler)

        return


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
    def __init__(self, file_name):
        self.log = logging.getLogger(file_name)
        self.log.setLevel(logging.DEBUG)

        self.log_file_path = path.join('.', 'log')
        if not path.exists(self.log_file_path):
            os.makedirs(self.log_file_path)

        self.LOG_FILE_NAME = file_name + '.log'
        self.LOG_FILE_FULL_PATH = path.join(self.log_file_path, self.LOG_FILE_NAME)

        formatter = logging.Formatter('[%(levelname)s | %(filename)s:%(lineno)s] %(asctime)s > %(message)s')

        file_handler = logging.FileHandler(self.LOG_FILE_FULL_PATH)
        stream_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self.log.addHandler(file_handler)
        self.log.addHandler(stream_handler)

        return


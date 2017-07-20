from os import path
import shutil
import os
from main.DbContract import *
from main.logger import Logger


def clean_up():
    print(DBContract.DB_PATH)
    if os.path.exists(DBContract.DB_PATH):
        shutil.rmtree(DBContract.DB_PATH)

    # print(Logger.LOG_PATH)
    # if os.path.exists(Logger.LOG_PATH):
    #     shutil.rmtree(Logger.LOG_PATH)


if __name__ == '__main__':
    clean_up()

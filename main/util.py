import shutil
import os
from main.DbContract import *


def clean_up():
    if os.path.exists(DBContract.DB_PATH):
        shutil.rmtree(DBContract.DB_PATH)


def print_table(rows):
    for i in rows:
        print(i)


def print_parse_items(items):
    for item in items:
        print(item)


if __name__ == '__main__':
    clean_up()

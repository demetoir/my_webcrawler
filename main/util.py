import shutil
import os
from main.DbContract import *


def clean_up():
    if os.path.exists(DBContract.DB_PATH):
        shutil.rmtree(DBContract.DB_PATH)


def print_rows(rows):
    print('total = %d' % len(rows))
    for row in rows:
        print(row)
    print()


def print_parse_items(items):
    for item in items:
        print(item)


if __name__ == '__main__':
    clean_up()

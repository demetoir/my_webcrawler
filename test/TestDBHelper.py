import os
import sqlite3

from nose import with_setup

from main.DbContract import *
from main.DbHelper import DbHelper
from main.Parser import Parser
from main.util import clean_up

URL_SITE = """http://bbs.ruliweb.com/best/humor?&page=%d"""


# TODO implement
def setup_func():
    # delete db, log
    clean_up()


# TODO implement
def teardown_func():
    clean_up()


def test_00__init__():

    DbHelper()

@with_setup(setup_func, teardown_func)
def test_01_init_db():
    helper = DbHelper()

    def _create_table_():
        with sqlite3.connect(DBContract.DB_FULL_PATH) as conn:
            # create each table
            for key in DBContract.CONTRACTS:
                sql = DBContract.CONTRACTS[key].SQL_CREATE_TABLE
                conn.execute(sql)
                helper.log.info(key + 'created')

    try:
        # make db dir
        if not os.path.exists(DBContract.DB_PATH):
            os.mkdir(DBContract.DB_PATH)

        _create_table_()
    except sqlite3.Error as e:
        helper.log.error(e)

@with_setup(setup_func, teardown_func)
def test_02_insert_items():
    parser = Parser()

    items = []
    for i in range(1, 2 + 1):
        res = parser.parse_ruliweb(URL_SITE % i)
        items += res

    db_helper = DbHelper()
    db_contract = DBContract()
    table_name = NewFeedContract.TABLE_NAME

    res = db_helper.insert_items(table_name, items)
    assert (res is True, "insert fail")

@with_setup(setup_func, teardown_func)
def test_03_query_all():
    parser = Parser()

    items = []
    for i in range(1, 2 + 1):
        res = parser.parse_ruliweb(URL_SITE % i)
        items += res

    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME

    res = db_helper.insert_items(table_name, items)
    assert (res is True, "insert fail")

    rows = db_helper.query_all(table_name)
    assert (rows is not None, "query all fail")

    if rows is not None:
        for i in rows:
            print(i)

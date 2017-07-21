from nose import with_setup
from main.DbContract import *
from main.DbHelper import DbHelper
from main.Parser import Parser
from main import util

URL_SITE = """http://bbs.ruliweb.com/best/humor?&page=%d"""


def setup_func():
    util.clean_up()
    pass


def teardown_func():
    pass


@with_setup(setup_func, teardown_func)
def test_00__init__():
    DbHelper()


@with_setup(setup_func, teardown_func)
def test_01_init_db():
    DbHelper()


@with_setup(setup_func, teardown_func)
def test_02_insert_items():
    parser = Parser()

    items = []
    for i in range(1, 2 + 1):
        res = parser.parse_ruliweb(URL_SITE % i)
        items += res

    items.sort(key=lambda item: item[NewFeedContract.KW_URL])
    util.print_parse_items(items)

    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME

    db_helper.insert_items(table_name, items)

    util.print_table(items)


@with_setup(setup_func, teardown_func)
def test_03_query_all():
    parser = Parser()

    items = []
    for i in range(1, 2 + 1):
        res = parser.parse_ruliweb(URL_SITE % i)
        items += res

    items.sort(key=lambda item: item[NewFeedContract.KW_URL])

    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME

    db_helper.insert_items(table_name, items)

    rows = db_helper.query_all(table_name)

    util.print_table(rows)

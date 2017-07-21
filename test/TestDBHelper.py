from nose import with_setup
from main.DbContract import *
from main.DbHelper import DbHelper
from main.Parser import Parser
from main import util

URL_SITE = """http://bbs.ruliweb.com/best/humor?&page=%d"""
SITE_NAME = """루리웹"""
CATEGORY = """유머 best"""


def update_db(max_page):
    total_inserted_count = 0
    # parse
    parser = Parser()
    for i in range(1, max_page + 1):
        items = parser.parse_ruliweb(URL_SITE % i)

        # add category, site_name
        for item in items:
            item[NewFeedContract.KW_CATEGORY] = CATEGORY
            item[NewFeedContract.KW_SITE_NAME] = SITE_NAME

        # insert to db
        db_helper = DbHelper()
        table_name = NewFeedContract.TABLE_NAME
        inserted_count = db_helper.insert_items(table_name, items)
        total_inserted_count += inserted_count
        if inserted_count == 0:
            break

    return total_inserted_count


def setup_func():
    # util.clean_up()
    pass


def teardown_func():
    pass


@with_setup(setup_func, teardown_func)
def test_00_update_db():
    max_page = 10
    cnt = update_db(max_page)
    print("total inserted count =", cnt)


@with_setup(setup_func, teardown_func)
def test_01_init_db():
    DbHelper()


@with_setup(setup_func, teardown_func)
def test_02_insert_items():
    print("pass")
    pass


@with_setup(setup_func, teardown_func)
def test_03_query_all():
    # insert to db
    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME

    # query all
    rows = db_helper.query_all(table_name).fetchall()

    # assertion query all
    if len(rows) == 0:
        util.print_table(rows)


@with_setup(setup_func, teardown_func)
def test_04_query_limit():
    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME
    limit_number = 10

    # query limit
    rows = db_helper.query_limit(table_name, limit_number).fetchall()

    # assertion query all
    if len(rows) == 0:
        print("limit number =", limit_number)
        util.print_table(rows)


@with_setup(setup_func, teardown_func)
def test_05_query_checked_item():
    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME

    # get check id, old row
    check_id = -1
    old_row = None
    rows = db_helper.query_limit(table_name, 1)
    for i in rows:
        check_id = i[NewFeedContract.IDX_ID]
        old_row = i
    print("check id = %d" % check_id)

    # check
    db_helper.query_check_item(table_name, check_id)

    # print all
    new_row = None
    rows = db_helper.query_limit(table_name, 1)
    for i in rows:
        new_row = i

    if old_row == new_row:
        print("old_row", old_row)
        print("new_row", new_row)
        raise AssertionError


@with_setup(setup_func, teardown_func)
def test_06_query_unchecked_item():
    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME

    # get check id
    check_id = -1
    rows = db_helper.query_limit(table_name, 1)
    for i in rows:
        check_id = i[0]

    # query check item
    db_helper.query_check_item(table_name, check_id)

    # get old row
    old_row = None
    rows = db_helper.query_limit(table_name, 1).fetchall()
    for i in rows:
        old_row = i

    # assertion query check item
    if old_row[NewFeedContract.IDX_IS_CHECKED] != 1:
        print("check id = %d" % check_id)
        print("old_row", old_row)
        print("check item fail")
        raise AssertionError

    # uncheck item
    db_helper.query_uncheck_item(table_name, check_id)

    # get new row
    new_row = None
    rows = db_helper.query_limit(table_name, 1).fetchall()
    for i in rows:
        new_row = i

    # assertion query uncheck item
    if old_row == new_row:
        print("check id = %d" % check_id)
        print("old_row", old_row)
        print("new_row", new_row)
        print("uncheck item fail")
        raise AssertionError


@with_setup(setup_func, teardown_func)
def test_07_delete_by_id():
    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME

    # get old row count
    rows = db_helper.query_all(table_name).fetchall()
    old_row_count = len(rows)

    # get delete item id
    delete_id = -1
    cursor = db_helper.query_limit(table_name, 1)
    for row in cursor:
        delete_id = row[NewFeedContract.IDX_ID]
    print("delete id = %d" % delete_id)

    # delete by id
    db_helper.delete_by_id(table_name, delete_id)

    # get new row count
    rows = db_helper.query_all(table_name).fetchall()
    new_row_count = len(rows)

    # assertion

    if new_row_count != old_row_count - 1:
        print("delete id =", delete_id)
        print("old_row_count =", old_row_count)
        print("new_row_count =", new_row_count)
        print("delete by id fail")
        raise AssertionError



# end

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
    rows = db_helper.query_all(table_name, limit=limit_number).fetchall()

    # assertion query all
    if len(rows) == 0:
        print("limit number =", limit_number)
        util.print_table(rows)


@with_setup(setup_func, teardown_func)
def test_05_update_is_check():
    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME
    idx = NewFeedContract.IDX_IS_CHECKED

    # get check id, old row
    check_ids = []
    old_rows = db_helper.query_all(table_name, limit=10).fetchall()
    for row in old_rows:
        check_ids += [row[NewFeedContract.IDX_ID]]

    db_helper.update_is_check(table_name, check_ids, 1)

    # get new row
    rows = db_helper.query_all(table_name, limit=10).fetchall()

    # assertion is_check == 1
    fine = True
    if not (len(rows) == 10):
        fine = False
    for row in rows:
        if row[NewFeedContract.IDX_IS_CHECKED] == 0:
            fine = False

    if not fine:
        print("update_is_check is_checked = 1 limit = 10 fail")
        print("rows len =", len(rows))

        print('rows')
        for row in rows:
            print(row)
        print()

        raise AssertionError

    # uncheck
    db_helper.update_is_check(table_name, check_ids, 0)

    # get new row
    rows = db_helper.query_all(table_name, limit=10).fetchall()

    # assertion
    fine = True
    if not (len(rows) == 10):
        fine = False
    for row in rows:
        if row[NewFeedContract.IDX_IS_CHECKED] == 1:
            fine = False

    if not fine:
        print("update_is_check is_checked = 0 limit = 10 fail")
        print("rows len =", len(rows))

        print('rows')
        for row in rows:
            print(row)
        print()

        raise AssertionError


@with_setup(setup_func, teardown_func)
def test_06_query_unchecked_item():
    pass


@with_setup(setup_func, teardown_func)
def test_07_delete_by_ids():
    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME

    # get old row count
    rows = db_helper.query_all(table_name).fetchall()
    old_row_count = len(rows)

    # get delete item ids
    delete_number = 10
    delete_ids = []
    cursor = db_helper.query_all(table_name, limit=delete_number)
    for row in cursor:
        delete_ids += [row[NewFeedContract.IDX_ID]]

    # delete by id
    db_helper.delete_by_ids(table_name, delete_ids)

    # get new row count
    rows = db_helper.query_all(table_name).fetchall()
    new_row_count = len(rows)

    # assertion delete by ids
    if new_row_count != old_row_count - delete_number:
        print("delete id")
        for id_ in delete_ids:
            print(id_)
        print()

        print("old_row_count =", old_row_count)
        print("new_row_count =", new_row_count)
        print("delete by ids fail")
        raise AssertionError


@with_setup(setup_func, teardown_func)
def test_08_query_by_urls():
    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME
    idx_url = NewFeedContract.IDX_URL

    # get urls
    old_rows = db_helper.query_all(table_name, limit=10).fetchall()
    urls = []
    for row in old_rows:
        urls += [row[idx_url]]

    # query by urls
    new_rows = db_helper.query_by_urls(table_name, urls, limit=5).fetchall()
    query_urls = []
    for row in new_rows:
        query_urls += [row[idx_url]]

    # assertion
    fine = True
    for url in query_urls:
        if url not in urls:
            fine = False
            break

    if not fine or len(new_rows) != 5:
        print('old_rows')
        util.print_table(old_rows)
        print()

        print('new_rows')
        util.print_table(new_rows)
        print()

        print('urls')
        for i in urls:
            print(i)
        print()

        print('query_urls')
        for i in query_urls:
            print(i)
        print()

        raise AssertionError


@with_setup(setup_func, teardown_func)
def test_09_query_by_is_checked():
    db_helper = DbHelper()
    table = NewFeedContract.TABLE_NAME
    idx = NewFeedContract.IDX_IS_CHECKED

    # get total_row_count
    rows = db_helper.query_all(table, ).fetchall()
    total_row_count = len(rows)

    # set 10 row is_check to 1
    rows = db_helper.query_all(table, limit=10).fetchall()
    ids = [row[DBContract.CONTRACTS[table].IDX_ID] for row in rows]
    db_helper.update_is_check(table, ids, 1)

    # query is check = 1
    rows = db_helper.query_by_is_checked(table, 1).fetchall()

    if not (len(rows) == 10):
        print("query_by_is_checked fail")
        print("rows len expect %d" % 10)
        print("rows len =", len(rows))
        raise AssertionError

    # query is checked = 0
    rows = db_helper.query_by_is_checked(table, 0).fetchall()

    if not (len(rows) == total_row_count - 10):
        print("query_by_is_checked fail")
        print("rows len expect %d" % (total_row_count - 10))
        print("rows len =", len(rows))
        raise AssertionError

    # query is checked = 1 limit = 5
    rows = db_helper.query_by_is_checked(table, 1, 5).fetchall()

    if not (len(rows) == 5):
        print("query_by_is_checked fail")
        print("rows len expect %d" % 5)
        print("rows len =", len(rows))
        raise AssertionError

    # query is checked = 0 limit = 5
    rows = db_helper.query_by_is_checked(table, 0, 5).fetchall()

    if not (len(rows) == 5):
        print("query_by_is_checked fail")
        print("rows len expect %d" % 5)
        print("rows len =", len(rows))
        raise AssertionError

    # uncheck
    db_helper.update_is_check(table, ids, 0)

# end

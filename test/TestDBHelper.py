from nose import with_setup
from main.DbContract import *
from main.DbHelper import DbHelper
from main.Parser import Parser
from main import util

URL_SITE = """http://bbs.ruliweb.com/best/humor?&page=%d"""
SITE_NAME = """루리웹"""
CATEGORY = """유머 best"""


def update_db(max_page):
    parser = Parser()
    db_helper = DbHelper()
    total_inserted_count = 0

    # update website
    items = [{WebSiteContract.PH_CATEGORY: CATEGORY,
              WebSiteContract.PH_SITE_NAME: SITE_NAME,
              WebSiteContract.PH_LAST_FEED_URL: None,
              WebSiteContract.PH_CRAWLING_URL_FORMAT: URL_SITE}]
    db_helper.insert_website(items)

    # get website id
    website_id = -1
    rows = db_helper.query_website_by_site_name_and_category(SITE_NAME, CATEGORY).fetchall()
    for row in rows:
        website_id = row[WebSiteContract.IDX_ID]

    # update new feed table
    for i in range(1, max_page + 1):
        items = parser.parse_ruliweb(URL_SITE % i)
        for item in items:
            item[NewFeedContract.PH_WEBSITE_ID] = website_id

        # insert to db until insert nothing
        inserted_count = db_helper.insert_new_feed(items)
        total_inserted_count += inserted_count
        if inserted_count == 0:
            break

    return total_inserted_count


def setup_func():
    pass


def teardown_func():
    pass


@with_setup(setup_func, teardown_func)
def test_00_setup():
    return


@with_setup(setup_func, teardown_func)
def test_01_init_db():
    DbHelper()


@with_setup(setup_func, teardown_func)
def test_02_update_db():
    max_page = 10
    cnt = update_db(max_page)
    print("total inserted count =", cnt)


@with_setup(setup_func, teardown_func)
def test_03_query_website():
    # insert to db
    db_helper = DbHelper()

    # query website
    util.print_rows(db_helper.query_website().fetchall())

    # query limit
    rows = db_helper.query_website(limit=1).fetchall()
    util.print_rows(rows)
    if len(rows) != 1:
        print('query website limit fail')
        print('expect value 1')
        print('value %d' % len(rows))
        util.print_rows(rows)
        raise AssertionError


@with_setup(setup_func, teardown_func)
def test_03_query_new_feed():
    # insert to db
    db_helper = DbHelper()

    util.print_rows(db_helper.query_new_feed().fetchall())
    rows = db_helper.query_new_feed(limit=10).fetchall()
    util.print_rows(rows)
    if len(rows) != 10:
        print('query new feed limit fail')
        print('expect value 10')
        print('value %d' % len(rows))
        util.print_rows(rows)
        raise AssertionError


@with_setup(setup_func, teardown_func)
def test_03_query_new_feed_by_urls():
    db_helper = DbHelper()
    idx_url = NewFeedContract.IDX_URL

    # get urls
    old_rows = db_helper.query_new_feed(limit=10).fetchall()
    urls = []
    for row in old_rows:
        urls += [row[idx_url]]

    # query by urls
    new_rows = db_helper.query_new_feed_by_urls(urls, limit=5).fetchall()
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
        util.print_rows(old_rows)
        print()

        print('new_rows')
        util.print_rows(new_rows)
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
def test_03_query_by_is_checked():
    db_helper = DbHelper()

    # get total_row_count
    rows = db_helper.query_new_feed().fetchall()
    total_row_count = len(rows)

    # set 10 row is_check to 1
    rows = db_helper.query_new_feed(limit=10).fetchall()
    ids = [row[NewFeedContract.IDX_ID] for row in rows]
    db_helper.update_new_feed_is_check(ids, 1)

    # query is check = 1
    rows = db_helper.query_new_feed_by_is_checked(1).fetchall()

    if not (len(rows) == 10):
        print("query_by_is_checked fail")
        print("rows len expect %d" % 10)
        print("rows len =", len(rows))
        raise AssertionError

    # query is checked = 0
    rows = db_helper.query_new_feed_by_is_checked(0).fetchall()

    if not (len(rows) == total_row_count - 10):
        print("query_by_is_checked fail")
        print("rows len expect %d" % (total_row_count - 10))
        print("rows len =", len(rows))
        raise AssertionError

    # query is checked = 1 limit = 5
    rows = db_helper.query_new_feed_by_is_checked(1, limit=5).fetchall()

    if not (len(rows) == 5):
        print("query_by_is_checked fail")
        print("rows len expect %d" % 5)
        print("rows len =", len(rows))
        raise AssertionError

    # query is checked = 0 limit = 5
    rows = db_helper.query_new_feed_by_is_checked(0, limit=5).fetchall()
    if not (len(rows) == 5):
        print("query_by_is_checked fail")
        print("rows len expect %d" % 5)
        print("rows len =", len(rows))
        raise AssertionError

    # uncheck
    db_helper.update_new_feed_is_check(ids, 0)


@with_setup(setup_func, teardown_func)
def test_04_update_new_feed_is_check():
    db_helper = DbHelper()

    # get check id, old row
    check_ids = []
    old_rows = db_helper.query_new_feed(limit=10).fetchall()
    for row in old_rows[:5]:
        check_ids += [row[NewFeedContract.IDX_ID]]

    db_helper.update_new_feed_is_check(check_ids, 1)

    # assertion is_check == 1
    rows = db_helper.query_new_feed(limit=10).fetchall()
    fine = True
    if not (len(rows) == 10):
        fine = False

    for row in rows[:5]:
        if row[NewFeedContract.IDX_IS_CHECKED] != 1:
            fine = False

    for row in rows[5:]:
        if row[NewFeedContract.IDX_IS_CHECKED] != 0:
            fine = False

    if not fine:
        print("update_is_check is_checked = 1 limit = 10 fail")
        print("rows len =", len(rows))
        print('first 5 rows must is_check = 1')
        print('next 5 rows must is_check = 0')
        util.print_rows(rows)
        raise AssertionError

    # uncheck
    db_helper.update_new_feed_is_check(check_ids, 0)

    # assertion
    rows = db_helper.query_new_feed(limit=10).fetchall()
    fine = True
    if not (len(rows) == 10):
        fine = False
    for row in rows:
        if row[NewFeedContract.IDX_IS_CHECKED] != 0:
            fine = False

    if not fine:
        print("update_is_check is_checked = 0 limit = 10 fail")
        print("rows len =", len(rows))
        print('rows must be is_checked = 0')
        util.print_rows(rows)
        raise AssertionError


# TODO
@with_setup(setup_func, teardown_func)
def test_04_update_website___():
    raise AssertionError


@with_setup(setup_func, teardown_func)
def test_05_delete_new_feed():
    db_helper = DbHelper()

    # get old row count
    old_row_count = len(db_helper.query_new_feed().fetchall())

    # get delete item ids
    delete_number = 10
    delete_ids = []
    cursor = db_helper.query_new_feed(limit=delete_number)
    for row in cursor:
        delete_ids += [row[NewFeedContract.IDX_ID]]

    # delete by id
    db_helper.delete_new_feed(delete_ids)

    # get new row count
    rows = db_helper.query_new_feed().fetchall()
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
def test_05_delete_website():
    db_helper = DbHelper()

    # get old row count
    old_row_count = len(db_helper.query_website().fetchall())

    # get delete item ids
    delete_number = 1
    delete_ids = []
    cursor = db_helper.query_website(limit=delete_number)
    for row in cursor:
        delete_ids += [row[WebSiteContract.IDX_ID]]

    # delete by id
    db_helper.delete_website(delete_ids)

    # get new row count
    new_row_count = len(db_helper.query_website().fetchall())

    # assertion delete by ids
    if new_row_count != old_row_count - delete_number:
        print("delete id")
        for id_ in delete_ids:
            print(id_)
        print()

        util.print_rows(db_helper.query_website().fetchall())

        print("old_row_count =", old_row_count)
        print("new_row_count =", new_row_count)
        print("delete by ids fail")
        raise AssertionError


@with_setup(setup_func, teardown_func)
def test_99_last_tear_up():
    return

# end

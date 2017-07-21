from os import path

# util lambda
# make name string formatter
wrap_nf = lambda x: ':' + x.lower()

# string join for sql statement
join_str = lambda x: " ".join(x)

# TODO need refactor
URL_SIZE = 500
TITLE_SIZE = 200
CATEGORY_SIZE = 200
SITE_NAME_SIZE = 60


class NewFeedContract(object):
    # table name
    TABLE_NAME = 'NEW_FEED_TABLE'

    # COL == column
    COL_ID = 'ID'
    COL_URL = 'URL'
    COL_SITE_NAME = 'SITE_NAME'
    COL_CATEGORY = 'CATEGORY'
    COL_TITLE = 'TITLE'
    COL_IS_CHECKED = 'IS_CHECKED'

    # KW == keyword
    KW_ID = 'id'
    KW_URL = 'url'
    KW_SITE_NAME = 'site_name'
    KW_CATEGORY = 'category'
    KW_TITLE = 'title'
    KW_IS_CHECKED = 'is_checked'
    KW_LIMIT_NUMBER = 'limit_number'

    # PH == placeholder
    PH_ID = wrap_nf(COL_ID)
    PH_URL = wrap_nf(COL_URL)
    PH_SITE_NAME = wrap_nf(COL_SITE_NAME)
    PH_CATEGORY = wrap_nf(COL_CATEGORY)
    PH_TITLE = wrap_nf(COL_TITLE)
    PH_IS_CHECKED = wrap_nf(COL_IS_CHECKED)
    PH_LIMIT_NUMBER = wrap_nf(KW_LIMIT_NUMBER)
    PH_TABLE_NAME = wrap_nf(TABLE_NAME)

    # index of column
    IDX_ID = 0
    IDX_URL = 1
    IDX_SITE_NAME = 2
    IDX_CATEGORY = 3
    IDX_TITLE = 4
    IDX_IS_CHECKED = 5

    # SQL statement
    # create table
    SQL_CREATE_TABLE = join_str([
        'CREATE TABLE %s (' % TABLE_NAME,
        '%s INTEGER PRIMARY KEY AUTOINCREMENT,' % COL_ID,
        '%s CHAR(%d) UNIQUE,' % (COL_URL, URL_SIZE),
        '%s CHAR(%d),' % (COL_SITE_NAME, SITE_NAME_SIZE),
        '%s CHAR(%d),' % (COL_CATEGORY, CATEGORY_SIZE),
        '%s CHAR(%d),' % (COL_TITLE, TITLE_SIZE),
        "%s INTEGER check( %s >= 0 AND %s<= 1 )" % (COL_IS_CHECKED, COL_IS_CHECKED, COL_IS_CHECKED),
        ")"
    ])

    # insert item
    SQL_INSERT = join_str([
        'INSERT INTO %s' % TABLE_NAME,
        '( %s, %s, %s, %s, %s )' % (COL_URL, COL_SITE_NAME, COL_TITLE, COL_CATEGORY, COL_IS_CHECKED),
        'VALUES ( %s, %s, %s, %s, 0)' % (PH_URL, PH_SITE_NAME, PH_TITLE, PH_CATEGORY)
    ])

    # query
    SQL_QUERY_ALL = join_str([
        'SELECT *',
        'FROM %s' % TABLE_NAME,
        'ORDER BY %s desc' % COL_URL
    ])

    SQL_QUERY_LIMIT = join_str([
        'SELECT *',
        'FROM %s' % TABLE_NAME,
        'ORDER BY %s desc' % COL_URL,
        'limit %s' % PH_LIMIT_NUMBER
    ])

    SQL_QUERY_BY_URL = join_str([
        'SELECT *',
        'FROM', TABLE_NAME,
        'WHERE', COL_URL, '=', PH_URL,
        'ORDER BY %s desc' % COL_URL
    ])

    # TODO test
    SQL_QUERY_BY_UNCHECKED_ALL = join_str([
        'SELECT *',
        'FROM %s' % TABLE_NAME,
        'WHERE %s = 0' % PH_IS_CHECKED,
        'ORDER BY %s desc' % COL_URL
    ])

    # TODO test
    SQL_QUERY_UNCHECKED_LIMIT = join_str([
        'SELECT *',
        'FROM %s' % TABLE_NAME,
        'WHERE %s = 0' % PH_IS_CHECKED,
        'ORDER BY %s desc' % COL_URL,
        'LIMIT %s' % PH_LIMIT_NUMBER
    ])

    # TODO test
    SQL_QUERY_CHECKED_ALL = join_str([
        'SELECT *',
        'FROM', TABLE_NAME,
        'WHERE', 'COL_IS_CHECKED', '= 1',
        'ORDER BY', COL_ID
    ])

    # TODO test
    SQL_QUERY_CHECKED_LIMIT = join_str([
        'SELECT *',
        'FROM', TABLE_NAME,
        'WHERE', COL_IS_CHECKED, '= 1',
        'LIMIT', PH_LIMIT_NUMBER,
        'ORDER BY', COL_ID
    ])

    # update item
    SQL_CHECK_ITEM = join_str([
        'UPDATE %s' % TABLE_NAME,
        'SET %s = 1' % COL_IS_CHECKED,
        'WHERE %s = %s' % (COL_ID, PH_ID)
    ])

    SQL_UNCHECK_ITEM = join_str([
        'UPDATE %s' % TABLE_NAME,
        'SET %s = 0' % COL_IS_CHECKED,
        'WHERE %s = %s' % (COL_ID, PH_ID)
    ])

    # delete item
    SQL_DELETE_BY_ID = join_str([
        "DELETE",
        "FROM %s" % TABLE_NAME,
        "WHERE %s = %s" % (COL_ID, PH_ID)
    ])


class LastFeedContract(object):
    # table name
    TABLE_NAME = 'LAST_FEED_TABLE'

    # COL == column
    COL_ID = 'ID'
    COL_SITE_NAME = 'SITE_NAME'
    COL_CATEGORY = 'CATEGORY'
    COL_NEW_FEED_ID = 'NEW_FEED_ID'

    # KW == keyword
    KW_ID = 'id'
    KW_SITE_NAME = 'site_name'
    KW_CATEGORY = 'category'
    KW_NEW_FEED_ID = 'new_feed_id'

    # PH == placeholder
    PH_ID = wrap_nf(COL_ID)
    PH_SITE_NAME = wrap_nf(COL_SITE_NAME)
    PH_CATEGORY = wrap_nf(COL_CATEGORY)
    PH_NEW_FEED_ID = wrap_nf(COL_NEW_FEED_ID)
    PH_TABLE_NAME = wrap_nf(TABLE_NAME)

    # index of column
    IDX_ID = 0
    IDX_SITE_NAME = 1
    IDX_CATEGORY = 2
    IDX_NEW_FEED_ID = 3

    # sql statement
    # TODO test
    SQL_CREATE_TABLE = join_str([
        'CREATE TABLE %s (' % TABLE_NAME,
        '%s INTEGER PRIMARY KEY AUTOINCREMENT,' % COL_ID,
        '%s CHAR(%d),' % (COL_SITE_NAME, SITE_NAME_SIZE),
        '%s CHAR(%d),' % (COL_CATEGORY, CATEGORY_SIZE),
        '%s INTEGER' % COL_NEW_FEED_ID,
        ')'
    ])


class DBContract(object):
    # db info
    DB_NAME = 'crawler.db'
    DB_FOLDER_NAME = 'db'
    DB_FULL_PATH = path.join('.', DB_FOLDER_NAME, DB_NAME)
    DB_PATH = path.join('.', DB_FOLDER_NAME)

    # DB each table's contracts
    # TODO change to automatically apply when db schema changed
    CONTRACTS = {
        NewFeedContract.TABLE_NAME: NewFeedContract,
        LastFeedContract.TABLE_NAME: LastFeedContract
    }

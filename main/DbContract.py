from os import path


# util lambda
# make name string formatter
def wrap(s):
    return ':' + s


class WebSiteContract(object):
    # table name
    TABLE_NAME = 'LAST_FEED_TABLE'

    ID = 'ID'
    SITE_NAME = 'SITE_NAME'
    CATEGORY = 'CATEGORY'
    LAST_FEED_URL = 'LAST_FEED_URL'
    CRAWLING_URL_FORMAT = 'CRAWLING_URL_FORMAT'

    # PH == placeholder
    PH_ID = 'id'
    PH_SITE_NAME = 'site_name'
    PH_CATEGORY = 'category'
    PH_LAST_FEED_URL = 'LAST_FEED_URL'
    PH_CRAWLING_URL_FORMAT = 'crawling_url_format'

    # WPH == wrapped placeholder
    WPH_ID = wrap(PH_ID)
    WPH_SITE_NAME = wrap(PH_SITE_NAME)
    WPH_CATEGORY = wrap(PH_CATEGORY)
    WPH_LAST_FEED_URL = wrap(PH_LAST_FEED_URL)
    WPH_CRAWLING_URL_FORMAT = wrap(PH_CRAWLING_URL_FORMAT)

    # index of column
    IDX_ID = 0
    IDX_SITE_NAME = 1
    IDX_CATEGORY = 2
    IDX_NEW_FEED_ID = 3
    IDX_CRAWLING_URL_FORMAT = 4

    CRAWLING_URL_FORMAT_SIZE = 500
    LAST_FEED_URL_SIZE = 500
    CATEGORY_SIZE = 200
    SITE_NAME_SIZE = 60

    PH_LIMIT_NUMBER = 'limit_number'
    WPH_LIMIT_NUMBER = wrap(PH_LIMIT_NUMBER)

    SQL_LIMIT = 'LIMIT %s' % WPH_LIMIT_NUMBER

    # sql statement
    SQL_CREATE_TABLE = " ".join([
        'CREATE TABLE %s (' % TABLE_NAME,
        '%s INTEGER PRIMARY KEY AUTOINCREMENT,' % ID,
        '%s CHAR(%d),' % (SITE_NAME, SITE_NAME_SIZE),
        '%s CHAR(%d),' % (CATEGORY, CATEGORY_SIZE),
        '%s CHAR(%d),' % (LAST_FEED_URL, LAST_FEED_URL_SIZE),
        '%s CHAR(%d)' % (CRAWLING_URL_FORMAT, CRAWLING_URL_FORMAT_SIZE),
        ')'
    ])

    SQL_INSERT = ' '.join([
        'insert into %s' % TABLE_NAME,
        '(%s, %s, %s, %s)'
        % (SITE_NAME, CATEGORY, LAST_FEED_URL,
           CRAWLING_URL_FORMAT),
        ' values(%s, %s, %s, %s)'
        % (WPH_SITE_NAME, WPH_CATEGORY, WPH_LAST_FEED_URL,
           WPH_CRAWLING_URL_FORMAT)
    ])

    SQL_UPDATE_SET_LAST_FEED_URL = '%s = %s' % (
        LAST_FEED_URL, WPH_LAST_FEED_URL)
    SQL_UPDATE_SET_SITE_NAME = '%s = %s' % (SITE_NAME, WPH_SITE_NAME)
    SQL_UPDATE_SET_CATEGORY = '%s = %s' % (CATEGORY, WPH_CATEGORY)
    SQL_UPDATE_SET_CRAWLING_URL_FORMAT = '%s = %s' % (
        CRAWLING_URL_FORMAT, WPH_CATEGORY)
    SQL_UPDATE = ' '.join([
        'update %s' % TABLE_NAME,
        'set %s = %s' % (LAST_FEED_URL, WPH_LAST_FEED_URL),
        'where %s = %s' % (ID, WPH_ID)
    ])

    SQL_DELETE = ' '.join([
        'delete from %s' % TABLE_NAME,
        'where %s = %s' % (ID, WPH_ID)
    ])

    SQL_QUERY = ' '.join([
        'select *',
        'from %s' % TABLE_NAME
    ])

    SQL_QUERY_BY_ID = ' '.join([
        'select *',
        'from %s' % TABLE_NAME,
        'where %s = in (%s)' % (ID, '%s')
    ])

    SQL_QUERY_BY_SITE_NAME_AND_CATEGORY = ' '.join([
        'select *',
        'from %s' % TABLE_NAME,
        'where %s = %s' % (SITE_NAME, PH_SITE_NAME),
        'and %s = %s' % (CATEGORY, PH_CATEGORY)
    ])


class NewFeedContract(object):
    # table name
    TABLE_NAME = 'NEW_FEED_TABLE'

    # COL == column
    ID = 'ID'
    URL = 'URL'
    TITLE = 'TITLE'
    IS_CHECKED = 'IS_CHECKED'
    WEBSITE_ID = 'WEBSITE_ID'

    # PH == placeholder
    PH_ID = 'id'
    PH_URL = 'url'
    PH_TITLE = 'title'
    PH_IS_CHECKED = 'is_checked'
    PH_WEBSITE_ID = 'website_id'

    # WPH == wrapped placeholder
    WPH_ID = wrap(PH_ID)
    WPH_URL = wrap(PH_URL)
    WPH_TITLE = wrap(PH_TITLE)
    WPH_IS_CHECKED = wrap(PH_IS_CHECKED)
    WPH_WEBSITE_ID = wrap(PH_WEBSITE_ID)

    # index of column
    IDX_ID = 0
    IDX_URL = 1
    IDX_TITLE = 2
    IDX_IS_CHECKED = 3
    IDX_WEBSITE_ID = 4

    URL_SIZE = 500
    TITLE_SIZE = 200

    PH_LIMIT_NUMBER = 'limit_number'
    WPH_LIMIT_NUMBER = wrap(PH_LIMIT_NUMBER)

    SQL_LIMIT = 'LIMIT %s' % WPH_LIMIT_NUMBER
    SQL_ORDER_BY_URL = 'ORDER BY %s desc' % URL

    # create table
    SQL_CREATE_TABLE = " ".join([
        'CREATE TABLE %s (' % TABLE_NAME,
        '%s INTEGER PRIMARY KEY AUTOINCREMENT,' % ID,
        '%s CHAR(%d) UNIQUE,' % (URL, URL_SIZE),
        '%s CHAR(%d),' % (TITLE, TITLE_SIZE),
        "%s INTEGER check( %s >= 0 AND %s<= 1 ),"
        % (IS_CHECKED, IS_CHECKED, IS_CHECKED),
        "%s INTEGER," % WEBSITE_ID,
        "FOREIGN KEY(%s) REFERENCES %s(%s)"
        % (WEBSITE_ID, WebSiteContract.TABLE_NAME, WebSiteContract.ID),
        ")"
    ])

    # insert
    SQL_INSERT = " ".join([
        'INSERT INTO %s' % TABLE_NAME,
        '( %s, %s, %s, %s)' % (
            URL, TITLE, IS_CHECKED, WEBSITE_ID),
        'VALUES ( %s, %s, 0, %s)' % (WPH_URL, WPH_TITLE, WPH_WEBSITE_ID)
    ])

    # update
    SQL_UPDATE_IS_CHECK = " ".join([
        'UPDATE %s' % TABLE_NAME,
        'SET %s = %s' % (IS_CHECKED, WPH_IS_CHECKED),
        'WHERE %s = %s' % (ID, WPH_ID)
    ])

    # delete
    SQL_DELETE = " ".join([
        "DELETE",
        "FROM %s" % TABLE_NAME,
        "WHERE %s = %s" % (ID, WPH_ID)
    ])

    # query
    SQL_QUERY = " ".join([
        'SELECT *',
        'FROM %s' % TABLE_NAME,
        SQL_ORDER_BY_URL
    ])

    SQL_QUERY_BY_URL = " ".join([
        'SELECT *',
        'FROM %s' % TABLE_NAME,
        'WHERE %s in (%s)' % (URL, '%s'),
        SQL_ORDER_BY_URL
    ])

    SQL_QUERY_BY_IS_CHECKED = " ".join([
        'SELECT *',
        'FROM %s' % TABLE_NAME,
        'WHERE %s = %s' % (IS_CHECKED, WPH_IS_CHECKED),
        SQL_ORDER_BY_URL
    ])


class DBContract(object):
    # db info
    DB_NAME = 'crawler.db'
    DB_FOLDER_NAME = 'db'
    DB_FULL_PATH = path.join('.', DB_FOLDER_NAME, DB_NAME)
    DB_PATH = path.join('.', DB_FOLDER_NAME)

    PH_LIMIT_NUMBER = 'limit_number'
    WPH_LIMIT_NUMBER = wrap(PH_LIMIT_NUMBER)

    CONTRACTS = [WebSiteContract, NewFeedContract]

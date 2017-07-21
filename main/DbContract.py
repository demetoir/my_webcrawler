from os import path

# util lambda
# make name string formatter
wrap_nf = lambda x: ':' + x.lower()

# string join for sql statement
join_str = lambda x: " ".join(x)


# TODO add keyword of sql
class SQL(object):
    CREATE_TABLE = "CREATE_TABLE"
    INSERT_INTO = "INSERT INTO"
    INTEGER = "INTEGER"
    CHAR = "CHAR"
    PRIMARY_KEY = 'PRIMARY_KEY'
    AUTOINCREMENT = 'AUTOINCREMENT'
    UNIQUE = "UNIQUE"
    check = "check"
    AND = "AND"
    OR = "OR"

    def BRACKET(self, statement):
        return '(%s)' % str(statement)

    pass


# TODO need refactor
URL_SIZE = 500
TITLE_SIZE = 200


# TODO add column category
class NewFeedContract(object):
    def __repr__(self):
        return self.__class__.__name__

    # table name
    TABLE_NAME = 'NEW_FEED_TABLE'

    # COL == column
    COL_ID = 'ID'
    COL_URL = 'URL'
    COL_TITLE = 'TITLE'
    COL_IS_CHECKED = 'IS_CHECKED'

    # KW == keyword
    KW_ID = 'id'
    KW_URL = 'url'
    KW_TITLE = 'title'
    KW_IS_CHECKED = 'is_checked'
    KW_LIMIT_NUMBER = 'limit_number'

    # PH == placeholder
    PH_ID = wrap_nf(COL_ID)
    PH_URL = wrap_nf(COL_URL)
    PH_TITLE = wrap_nf(COL_TITLE)
    PH_IS_CHECKED = wrap_nf(COL_IS_CHECKED)
    PH_LIMIT_NUMBER = wrap_nf(KW_LIMIT_NUMBER)
    PH_TABLE_NAME = wrap_nf(TABLE_NAME)

    # SQL statement
    # create table
    SQL_CREATE_TABLE = join_str(
        ['CREATE TABLE %s (' % TABLE_NAME,
         '%s INTEGER PRIMARY KEY AUTOINCREMENT,' % COL_ID,
         '%s CHAR(%d) UNIQUE,' % (COL_URL, URL_SIZE),
         '%s CHAR(%d),' % (COL_TITLE, TITLE_SIZE),
         "%s INTEGER check( %s >= 0 AND %s<= 1 )" % (COL_IS_CHECKED, COL_IS_CHECKED, COL_IS_CHECKED),
         ")"]
    )

    # insert item
    SQL_INSERT = join_str(
        ['INSERT INTO %s' % TABLE_NAME,
         '( %s , %s , %s )' % (COL_URL, COL_TITLE, COL_IS_CHECKED),
         'VALUES ( %s , %s , 0)' % (PH_URL, PH_TITLE)]
    )

    # query item
    SQL_QUERY_ALL = join_str([
        'SELECT *',
        'FROM', TABLE_NAME,
        'ORDER BY', COL_ID])

    SQL_QUERY_LIMIT = join_str([
        'SELECT *',
        'FROM', TABLE_NAME,
        'ORDER BY', COL_ID,
        'limit', PH_LIMIT_NUMBER])

    SQL_QUERY_UNCHECKED_ALL = join_str(
        ['SELECT *',
         'FROM', TABLE_NAME,
         'WHERE', PH_IS_CHECKED, '= 0',
         'ORDER BY', PH_ID
         ])

    SQL_QUERY_UNCHECKED_LIMIT = join_str([
        'SELECT *',
        'FROM', TABLE_NAME,
        'WHERE', PH_IS_CHECKED, '= 0',
        'LIMIT', PH_LIMIT_NUMBER,
        'ORDER BY', COL_ID
    ])

    SQL_QUERY_CHECKED_ALL = join_str(
        ['SELECT *',
         'FROM', TABLE_NAME,
         'WHERE', 'COL_IS_CHECKED', '= 1',
         'ORDER BY', COL_ID])

    SQL_QUERY_CHECKED_LIMIT = join_str([
        'SELECT *',
        'FROM', TABLE_NAME,
        'WHERE', COL_IS_CHECKED, '= 1',
        'LIMIT', PH_LIMIT_NUMBER,
        'ORDER BY', COL_ID
    ])

    SQL_QUERY_BY_URL_AND_TITLE = join_str([
        'SELECT *',
        'FROM', TABLE_NAME,
        'WHERE', COL_URL, '=', PH_URL,
        'AND', COL_TITLE, '=', PH_URL,
    ])

    # update item
    SQL_CHECK_ITEM = join_str([
        'UPDATE', TABLE_NAME,
        'SET ', COL_IS_CHECKED, '= 1',
        'WHERE', COL_ID, '=', PH_ID
    ])

    SQL_UNCHECK_ITEM = join_str([
        'UPDATE', TABLE_NAME,
        'SET', COL_IS_CHECKED, '= 1',
        'WHERE', COL_ID, '=', PH_ID,
    ])


class LastFeedContract(object):
    def __repr__(self):
        return self.__class__.__name__

    # table name
    TABLE_NAME = 'LAST_FEED_TABLE'

    # COL == column
    COL_ID = 'ID'
    COL_URL = 'URL'

    # KW == keyword
    KW_ID = 'ID'
    KW_URL = 'URL'

    # PH == placeholder
    PH_ID = wrap_nf(COL_ID)
    PH_URL = wrap_nf(COL_URL)
    PH_TABLE_NAME = wrap_nf(TABLE_NAME)

    # sql statement
    # TODO implement
    SQL_CREATE_TABLE = join_str([
        'CREATE TABLE %s (' % TABLE_NAME,
        '%s INTEGER PRIMARY KEY AUTOINCREMENT,' % COL_ID,
        '%s CHAR(%d) UNIQUE' % (COL_URL, URL_SIZE),
        ')'
    ])


class SavedFeedContract(object):
    def __repr__(self):
        return self.__class__.__name__

    # table name
    TABLE_NAME = 'SAVED_FEED_TABLE'

    # COL == column
    COL_ID = 'ID'
    COL_URL = 'URL'
    COL_TITLE = 'TITLE'
    COL_IS_CHECKED = 'IS_CHECKED'

    # KW == keyword
    KW_ID = 'ID'
    KW_URL = 'URL'
    KW_TITLE = 'TITLE'
    KW_IS_CHECKED = 'IS_CHECKED'
    KW_LIMIT_NUMBER = 'LIMIT_NUMBER'

    # PH == placeholder
    PH_ID = wrap_nf(COL_ID)
    PH_URL = wrap_nf(COL_URL)
    PH_TITLE = wrap_nf(COL_TITLE)
    PH_IS_CHECKED = wrap_nf(COL_IS_CHECKED)
    PH_LIMIT_NUMBER = wrap_nf(KW_LIMIT_NUMBER)
    PH_TABLE_NAME = wrap_nf(TABLE_NAME)

    # sql statement
    # TODO implement
    SQL_CREATE_TABLE = join_str([
        'CREATE TABLE %s (' % TABLE_NAME,
        '%s INTEGER PRIMARY KEY AUTOINCREMENT,' % COL_ID,
        '%s CHAR(%d) UNIQUE,' % (COL_URL, URL_SIZE),
        '%s CHAR(%d),' % (COL_TITLE, TITLE_SIZE),
        "%s INTEGER check( %s >= 0 AND %s<= 1 )" % (COL_IS_CHECKED, COL_IS_CHECKED, COL_IS_CHECKED),
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
    CONTRACTS = {NewFeedContract.TABLE_NAME: NewFeedContract,
                 LastFeedContract.TABLE_NAME: LastFeedContract,
                 SavedFeedContract.TABLE_NAME: SavedFeedContract}

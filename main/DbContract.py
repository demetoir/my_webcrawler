from os import path


class DBContract(object):
    def __init__(self):
        pass

    DB_NAME = 'crawler.db'

    # TODO
    # DB_PATH =

    # column
    COLUMN_ID = 'ID'
    COLUMN_URL = 'URL'
    COLUMN_TITLE = 'TITLE'
    COLUMN_IS_CHECKED = 'IS_CHECKED'

    # placeholder
    PLACEHOLDER_TABLE_NAME = 'table_name'
    PLACEHOLDER_URL = 'url'
    PLACEHOLDER_TITLE = 'title'
    PLACEHOLDER_IS_CHECKED = 'is_checked'
    PLACEHOLDER_ID = 'id'
    PLACEHOLDER_LIMIT_NUMBER = 'limit_number'

    # table name list
    TABLE_NAME_LIST = ['ruliweb', 'buzzbee', 'schoolmusic', ]

    # create table
    SQL_CREATE_TABLE = """
    CREATE TABLE %(PLACEHOLDER_TABLE_NAME)s (
    %(COLUMN_ID)s INTEGER PRIMARY KEY AUTOINCREMENT,
    %(COLUMN_URL)s  CHAR(500) UNIQUE,
    %(COLUMN_TITLE)s CHAR(200),
    %(COLUMN_IS_CHECKED)s INTEGER check(%(COLUMN_IS_CHECKED)s >=0 AND %(COLUMN_IS_CHECKED)s <= 1)
    )""" % {
        "COLUMN_ID": COLUMN_ID,
        "COLUMN_URL": COLUMN_URL,
        "COLUMN_TITLE": COLUMN_TITLE,
        "COLUMN_IS_CHECKED": COLUMN_IS_CHECKED,
        "PLACEHOLDER_TABLE_NAME": "%s"
    }

    # insert item
    SQL_INSERT = """
    INSERT INTO 
    %(PLACEHOLDER_TABLE_NAME)s (%(COLUMN_URL)s, %(COLUMN_TITLE)s, %(COLUMN_IS_CHECKED)s) 
    VALUES (:%(PLACEHOLDER_URL)s , :%(PLACEHOLDER_TITLE)s, 0)
    """ % {"PLACEHOLDER_TABLE_NAME": "%s",
           "PLACEHOLDER_URL": PLACEHOLDER_URL,
           "PLACEHOLDER_TITLE": PLACEHOLDER_TITLE,
           "COLUMN_URL": COLUMN_URL,
           "COLUMN_TITLE": COLUMN_TITLE,
           "COLUMN_IS_CHECKED": COLUMN_IS_CHECKED
           }

    # query item
    SQL_QUERY_ALL = """
    SELECT * 
    FROM %(PLACEHOLDER_TABLE_NAME)s 
    ORDER BY %(COLUMN_ID)s 
    """ % {
        "PLACEHOLDER_TABLE_NAME": "%s",
        "COLUMN_ID": COLUMN_ID
    }

    SQL_QUERY_LIMIT = """
    SELECT * 
    FROM :%(PLACEHOLDER_TABLE_NAME)s
    LIMIT :%(PLACEHOLDER_LIMIT_NUMBER)s
    ORDER BY %(COLUMN_ID)s
    """ % {
        "PLACEHOLDER_TABLE_NAME": PLACEHOLDER_TABLE_NAME,
        "PLACEHOLDER_LIMIT_NUMBER": PLACEHOLDER_LIMIT_NUMBER,
        "COLUMN_ID": COLUMN_ID
    }

    SQL_QUERY_UNCHECKED_ALL = """
    SELECT * 
    FROM :%(PLACEHOLDER_TABLE_NAME)s
    WHERE %(COLUMN_IS_CHECKED)s = 0
    ORDER BY %(COLUMN_ID)s
    """ % {
        "PLACEHOLDER_TABLE_NAME": PLACEHOLDER_TABLE_NAME,
        "COLUMN_IS_CHECKED": COLUMN_IS_CHECKED,
        "COLUMN_ID": COLUMN_ID
    }

    SQL_QUERY_UNCHECKED_LIMIT = """
    SELECT * 
    FROM :%(PLACEHOLDER_TABLE_NAME)s
    WHERE %(COLUMN_IS_CHECKED)s = 0
    LIMIT :%(PLACEHOLDER_LIMIT_NUMBER)s
    ORDER BY %(COLUMN_ID)s
    """ % {
        "PLACEHOLDER_TABLE_NAME": PLACEHOLDER_TABLE_NAME,
        "PLACEHOLDER_LIMIT_NUMBER": PLACEHOLDER_LIMIT_NUMBER,
        "COLUMN_IS_CHECKED": COLUMN_IS_CHECKED,
        "COLUMN_ID": COLUMN_ID
    }

    SQL_QUERY_CHECKED_ALL = """
    SELECT * 
    FROM :%(PLACEHOLDER_TABLE_NAME)s
    WHERE %(COLUMN_IS_CHECKED)s = 1
    ORDER BY %(COLUMN_ID)s
    """ % {
        "PLACEHOLDER_TABLE_NAME": PLACEHOLDER_TABLE_NAME,
        "COLUMN_IS_CHECKED": COLUMN_IS_CHECKED,
        "COLUMN_ID": COLUMN_ID
    }

    SQL_QUERY_CHECKED_LIMIT = """
    SELECT * 
    FROM :%(PLACEHOLDER_TABLE_NAME)s
    WHERE %(COLUMN_IS_CHECKED)s = 1
    LIMIT :%(PLACEHOLDER_LIMIT_NUMBER)s
    ORDER BY %(COLUMN_ID)s
    """ % {
        "PLACEHOLDER_TABLE_NAME": PLACEHOLDER_TABLE_NAME,
        "PLACEHOLDER_LIMIT_NUMBER": PLACEHOLDER_LIMIT_NUMBER,
        "COLUMN_IS_CHECKED": COLUMN_IS_CHECKED,
        "COLUMN_ID": COLUMN_ID
    }

    SQL_QUERY_BY_URL_AND_TITLE = """
    SELECT * 
    FROM :%(PLACEHOLDER_TABLE_NAME)s
    WHERE %(COLUMN_URL)s = :%(PLACEHOLDER_URL)s AND %(COLUMN_TITLE)s = :%(PLACEHOLDER_URL)s
    """ % {
        "PLACEHOLDER_TABLE_NAME": PLACEHOLDER_TABLE_NAME,
        "PLACEHOLDER_URL": PLACEHOLDER_URL,
        "PLACEHOLDER_TITLE": PLACEHOLDER_TITLE,
        "COLUMN_URL": COLUMN_URL,
        "COLUMN_TITLE": COLUMN_TITLE
    }

    # update item
    SQL_CHECK_ITEM = """
    UPDATE :%(PLACEHOLDER_TABLE_NAME)s
    SET %(COLUMN_IS_CHECKED)s = 1
    WHERE %(COLUMN_ID)s = :%(PLACEHOLDER_ID)s
    """ % {
        "PLACEHOLDER_TABLE_NAME": PLACEHOLDER_TABLE_NAME,
        "PLACEHOLDER_ID": PLACEHOLDER_ID,
        "COLUMN_IS_CHECKED": COLUMN_IS_CHECKED,
        "COLUMN_ID": COLUMN_ID
    }

    SQL_UNCHECK_ITEM = """
    UPDATE :%(PLACEHOLDER_TABLE_NAME)s
    SET %(COLUMN_IS_CHECKED)s = 0
    WHERE %(COLUMN_ID)s = :%(PLACEHOLDER_ID)s
    """ % {
        "PLACEHOLDER_TABLE_NAME": PLACEHOLDER_TABLE_NAME,
        "PLACEHOLDER_ID": PLACEHOLDER_ID,
        "COLUMN_IS_CHECKED": COLUMN_IS_CHECKED,
        "COLUMN_ID": COLUMN_ID
    }

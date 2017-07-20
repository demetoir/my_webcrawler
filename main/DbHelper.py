import sqlite3

from main.DbContract import DBContract
from main.logger import Logger
import os


# TODO need to practice logging module
class DbHelper(object):
    MAX_QUERY_PAGE = 5

    def __init__(self, ):
        self.log = Logger(self.__class__.__name__).log
        self.init_db()
        return

    def __query__(self, sql, param=None):
        try:
            with sqlite3.connect(DBContract.DB_NAME) as conn:
                if param is not None:
                    rows = conn.execute(sql, param)
                else:
                    rows = conn.execute(sql)

        except sqlite3.Error as e:
            self.log.error(e)
            return None

        self.log.info("query success")
        return rows

    def __insert__(self, sql, param=None):
        try:
            with sqlite3.connect(DBContract.DB_NAME) as conn:
                if param is not None:
                    conn.execute(sql, param)
                else:
                    conn.execute(sql)

                conn.commit()
        except sqlite3.Error as e:
            self.log.error(e)
            return False

        self.log.info("insert success")
        return True

    def __insert_many__(self, sql, param_list):
        try:
            with sqlite3.connect(DBContract.DB_NAME) as conn:
                conn.executemany(sql, param_list)
                conn.commit()
        except sqlite3.Error as e:
            self.log.error(e)
            return None

        self.log.info("insert_many success, %d done" % len(param_list))
        return True

    def __create_table__(self):
        with sqlite3.connect(DBContract.DB_FULL_PATH) as conn:
            for table_name in DBContract.TABLE_NAME_LIST:
                # TODO need hack
                sql = DBContract.SQL_CREATE_TABLE % table_name
                conn.execute(sql)
                self.log.info("create table " + table_name)

    def init_db(self, ):
        try:
            if not os.path.exists(DBContract.DB_PATH):
                os.mkdir(DBContract.DB_PATH)

            self.__create_table__()
        except sqlite3.Error as e:
            self.log.error(e)

    # query
    def query_all(self, table_name):
        sql = DBContract.SQL_QUERY_ALL % table_name

        return self.__query__(sql, None)

    # TODO test
    def query_limit(self, table_name, max_query_item=MAX_QUERY_PAGE):
        sql = DBContract.SQL_QUERY_LIMIT
        param = {DBContract.PLACEHOLDER_TABLE_NAME: table_name,
                 DBContract.PLACEHOLDER_LIMIT_NUMBER: max_query_item, }

        return self.__query__(sql, param)

    # TODO test
    def query_uncheck_item(self, table_name, item_id, ):
        sql = DBContract.SQL_UNCHECK_ITEM
        param = {DBContract.PLACEHOLDER_TABLE_NAME: table_name,
                 DBContract.PLACEHOLDER_ID: item_id,
                 }

        return self.__query__(sql, param)

    # TODO test
    def query_check_item(self, table_name, item_id, ):
        sql = DBContract.SQL_CHECK_ITEM
        param = {DBContract.PLACEHOLDER_TABLE_NAME: table_name,
                 DBContract.PLACEHOLDER_ID: item_id,
                 }

        return self.__query__(sql, param)

    # insert
    def insert_items(self, table_name, items, ):
        sql = DBContract.SQL_INSERT % table_name

        # add table name
        for item in items:
            item[DBContract.PLACEHOLDER_TABLE_NAME] = table_name

        return self.__insert_many__(sql, items)

    # util
    @staticmethod
    def print_all():
        with sqlite3.connect(DBContract.DB_NAME) as conn:
            cur = conn.execute(DBContract.SQL_QUERY_ALL)

        for col in cur:
            print(col)
        print()

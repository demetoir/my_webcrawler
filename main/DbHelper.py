import sqlite3

from main.DbContract import *
from main.logger import Logger
import os


# TODO need to practice logging module
class DbHelper(object):
    MAX_QUERY_PAGE = 5

    def __init__(self, ):
        # load contracts
        self.contracts = {}
        for key in DBContract.CONTRACTS:
            self.contracts[key] = DBContract.CONTRACTS[key]

        self.log = Logger(self.__class__.__name__).log

        self._init_db_()
        return

    def _init_db_(self, ):
        try:
            if not os.path.exists(DBContract.DB_PATH):
                os.mkdir(DBContract.DB_PATH)

            self._create_table_()
        except sqlite3.Error as e:
            self.log.error(e)
            raise e

    def _create_table_(self):
        tables = self.get_tables()

        with sqlite3.connect(DBContract.DB_FULL_PATH) as conn:
            # create each table
            for key in DBContract.CONTRACTS:
                table_name = DBContract.CONTRACTS[key].TABLE_NAME
                if table_name not in tables:
                    sql = DBContract.CONTRACTS[key].SQL_CREATE_TABLE
                    conn.execute(sql)
                    self.log.info('%s created' % table_name)

    def _query_(self, sql, param=None):
        try:
            with sqlite3.connect(DBContract.DB_FULL_PATH) as conn:
                if param is not None:
                    rows = conn.execute(sql, param)
                else:
                    rows = conn.execute(sql)

        except sqlite3.Error as e:
            self.log.error(e)
            raise e

        self.log.info("query success")
        return rows

    def _insert_(self, sql, param=None):
        try:
            with sqlite3.connect(DBContract.DB_FULL_PATH) as conn:
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

    def _insert_many_(self, sql, param_list):
        try:
            with sqlite3.connect(DBContract.DB_FULL_PATH) as conn:
                conn.executemany(sql, param_list)
                conn.commit()
        except sqlite3.Error as e:
            self.log.error(e)
            raise e

        self.log.info("insert_many success, %d done" % len(param_list))
        return True

    # query
    def query_all(self, contract_name):
        sql = self.contracts[contract_name].SQL_QUERY_ALL
        return self._query_(sql, None)

    # TODO test
    def query_limit(self, contract_name, max_query_item=MAX_QUERY_PAGE):
        sql = self.contracts[contract_name].SQL_QUERY_LIMIT
        param = {NewFeedContract.KW_LIMIT_NUMBER: max_query_item}
        return self._query_(sql, param)

    # TODO test
    def query_uncheck_item(self, contract_name, item_id):
        sql = self.contracts[contract_name].SQL_UNCHECK_ITEM
        param = {self.contracts[contract_name].PLACEHOLDER_ID: item_id}
        return self._query_(sql, param)

    # TODO test
    def query_check_item(self, contract_name, item_id):
        sql = self.contracts[contract_name].SQL_CHECK_ITEM
        param = {self.contracts[contract_name].PLACEHOLDER_ID: item_id}
        return self._query_(sql, param)

    # insert
    def insert_items(self, contract_name, items):
        sql = self.contracts[contract_name].SQL_INSERT
        return self._insert_many_(sql, items)

    # util
    @staticmethod
    def print_all(contract_name):
        with sqlite3.connect(DBContract.DB_NAME) as conn:
            cur = conn.execute()

        for col in cur:
            print(col)
        print()

    # TODO refactor
    def get_tables(self):
        with sqlite3.connect(DBContract.DB_FULL_PATH) as conn:
            cursor = conn.cursor()
            sql = "SELECT name FROM SQLITE_MASTER WHERE type='table'"
            cursor.execute(sql)
            tables = [row[0] for row in cursor.fetchall()]

        return tables

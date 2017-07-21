import sqlite3

from main.DbContract import *
from main.logger import Logger
import os


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
                    cursor = conn.execute(sql, param)
                else:
                    cursor = conn.execute(sql)

        except sqlite3.Error as e:
            self.log.error(e)
            raise e

        return cursor

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

    def _insert_many_(self, sql, param_list):
        try:
            with sqlite3.connect(DBContract.DB_FULL_PATH) as conn:
                conn.executemany(sql, param_list)
                conn.commit()
        except sqlite3.Error as e:
            self.log.error(e)
            raise e

    def _update_(self, sql, param=None):
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

        return True

    def _delete_(self, sql, param=None):
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

        return True

    # query
    def query_all(self, table_name):
        sql = self.contracts[table_name].SQL_QUERY_ALL
        ret = self._query_(sql, None)
        self.log.info("query_all success")
        return ret

    def query_limit(self, table_name, max_query_item=MAX_QUERY_PAGE):
        sql = self.contracts[table_name].SQL_QUERY_LIMIT
        param = {NewFeedContract.KW_LIMIT_NUMBER: max_query_item}
        ret = self._query_(sql, param)
        self.log.info("query_limit success")
        return ret

    def query_url(self, table_name, url):
        sql = DBContract.CONTRACTS[table_name].SQL_QUERY_BY_URL
        param = {DBContract.CONTRACTS[table_name].KW_URL: url}
        ret = self._query_(sql, param)
        self.log.info("query_url success")
        return ret

    # insert
    def insert_items(self, table_name, items):
        # TODO optimize
        filtered_items = []
        for item in items:
            url = item[DBContract.CONTRACTS[table_name].KW_URL]
            rows = self.query_url(table_name, url).fetchall()
            if len(rows) == 0:
                filtered_items += [item]

        sql = self.contracts[table_name].SQL_INSERT
        self._insert_many_(sql, filtered_items)
        self.log.info("insert %d items success" % len(filtered_items))
        return len(filtered_items)

    # update
    def query_uncheck_item(self, table_name, item_id):
        sql = self.contracts[table_name].SQL_UNCHECK_ITEM
        param = {self.contracts[table_name].KW_ID: item_id}
        ret = self._update_(sql, param)
        self.log.info("query_uncheck_item success")
        return ret

    def query_check_item(self, table_name, item_id):
        sql = self.contracts[table_name].SQL_CHECK_ITEM
        param = {self.contracts[table_name].KW_ID: item_id}
        ret = self._update_(sql, param)
        self.log.info("query_check_item success")
        return ret

    # delete
    def delete_by_id(self, table_name, id):
        sql = DBContract.CONTRACTS[table_name].SQL_DELETE_BY_ID
        param = {DBContract.CONTRACTS[table_name].KW_ID: id}
        self._delete_(sql, param)
        self.log.info("delete success")

    # TODO refactor
    def get_tables(self):
        with sqlite3.connect(DBContract.DB_FULL_PATH) as conn:
            cursor = conn.cursor()
            sql = "SELECT name FROM SQLITE_MASTER WHERE type='table'"
            cursor.execute(sql)
            tables = [row[0] for row in cursor.fetchall()]

        return tables

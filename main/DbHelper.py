import sqlite3

from main.DbContract import *
from main.logger import Logger
import os


class DbHelper(object):
    MAX_QUERY_PAGE = 5

    def __init__(self, ):
        # load contracts
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
        tables = self.query_tables()

        with sqlite3.connect(DBContract.DB_FULL_PATH) as conn:
            # create each table
            for key in DBContract.CONTRACTS:
                table_name = DBContract.CONTRACTS[key].TABLE_NAME
                if table_name not in tables:
                    sql = DBContract.CONTRACTS[key].SQL_CREATE_TABLE
                    conn.execute(sql)
                    self.log.info('%s created' % table_name)

    def _execute_(self, sql, param=None, commit=False, many=False):
        try:
            with sqlite3.connect(DBContract.DB_FULL_PATH) as conn:
                if many:
                    execute = conn.executemany
                else:
                    execute = conn.execute

                if param is None:
                    cursor = execute(sql)
                else:
                    cursor = execute(sql, param)

                if commit:
                    conn.commit()
        except sqlite3.Error as e:
            self.log.error(e)
            raise e

        return cursor

    def _query_(self, sql, param=None):
        return self._execute_(sql, param)

    def _insert_(self, sql, param=None, many=False):
        return self._execute_(sql, param, commit=True, many=many)

    def _update_(self, sql, param=None, many=False):
        return self._execute_(sql, param, commit=True, many=many)

    def _delete_(self, sql, param=None, many=False):
        return self._execute_(sql, param, commit=True, many=many)

    # insert
    def insert_items(self, table, items):
        # todo hack, optimize
        pass

        # get insert urls
        key = DBContract.CONTRACTS[table].KW_URL
        insert_urls = [item[key] for item in items]

        # get exist_urls
        rows = self.query_by_urls(table, insert_urls).fetchall()
        idx = DBContract.CONTRACTS[table].IDX_URL
        exist_urls = [row[idx] for row in rows]

        # get filtered_items
        filtered_items = [item for item in items if item[key] not in exist_urls]

        # insert filtered_items
        sql = DBContract.CONTRACTS[table].SQL_INSERT
        self._insert_(sql, filtered_items, many=True)
        self.log.info("insert %d items success" % len(filtered_items))
        return len(filtered_items)

    # update
    def update_is_check(self, table, ids, value):
        sql = DBContract.CONTRACTS[table].SQL_UPDATE_CHECK_ITEM
        params = []
        for id_ in ids:
            params += [{
                DBContract.CONTRACTS[table].KW_ID: id_,
                DBContract.CONTRACTS[table].KW_IS_CHECKED: value
            }]

        ret = self._update_(sql, params, many=True)
        self.log.info("query_uncheck_item success")
        return ret

    # delete
    def delete_by_ids(self, table_name, ids):
        sql = DBContract.CONTRACTS[table_name].SQL_DELETE_BY_ID
        param = []
        for id_ in ids:
            param += [{DBContract.CONTRACTS[table_name].KW_ID: id_}]

        self._delete_(sql, param, many=True)
        self.log.info("delete success")

    # query
    def query_all(self, table, limit=-1):
        sql = DBContract.CONTRACTS[table].SQL_QUERY_ALL
        if limit == -1:
            ret = self._query_(sql, None)
        else:
            sql += DBContract.CONTRACTS[table].SQL_LIMIT
            param = {NewFeedContract.KW_LIMIT_NUMBER: limit}
            ret = self._query_(sql, param)

        self.log.info("query_all success")
        return ret

    def query_by_urls(self, table, urls, limit=-1):
        # TODO hack
        # build sql statement and param
        kw = DBContract.CONTRACTS[table].KW_IS_CHECKED
        kw_list = [kw + str(i) for i in range(len(urls))]
        ph_list = [':' + kw + str(i) for i in range(len(urls))]
        str_ph = ','.join(ph_list)
        sql = DBContract.CONTRACTS[table].SQL_QUERY_BY_URL % str_ph
        param = {ph: url for ph, url in zip(kw_list, urls)}

        if limit == -1:
            ret = self._query_(sql, param)
        else:
            # add limit statement and param
            sql += DBContract.CONTRACTS[table].SQL_LIMIT
            param[DBContract.CONTRACTS[table].KW_LIMIT_NUMBER] = limit
            ret = self._query_(sql, param)
            pass
        self.log.info("query_by_urls success")
        return ret

    def query_by_is_checked(self, table, value, limit=-1):
        sql = DBContract.CONTRACTS[table].SQL_QUERY_BY_IS_CHECKED
        param = {DBContract.CONTRACTS[table].KW_IS_CHECKED: value}
        if limit == -1:
            ret = self._query_(sql, param)
        else:
            sql += DBContract.CONTRACTS[table].SQL_LIMIT
            param[DBContract.CONTRACTS[table].KW_LIMIT_NUMBER] = limit
            ret = self._query_(sql, param)

        self.log.info("query_by_is_checked success")
        return ret

    def query_tables(self):
        sql = "SELECT name FROM SQLITE_MASTER WHERE TYPE='table'"
        rows = self._query_(sql, None).fetchall()
        return [row[0] for row in rows]

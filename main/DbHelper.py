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
            for contract in DBContract.CONTRACTS:
                if contract.TABLE_NAME not in tables:
                    conn.execute(contract.SQL_CREATE_TABLE)
                    self.log.info('%s table created' % contract.TABLE_NAME)

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
    def insert_new_feed(self, items):
        # get insert urls
        key = NewFeedContract.PH_URL
        insert_urls = [item[key] for item in items]

        # get exist_urls
        rows = self.query_new_feed_by_urls(insert_urls).fetchall()
        idx = NewFeedContract.IDX_URL
        exist_urls = [row[idx] for row in rows]

        # get filtered_items
        filtered_items = [item for item in items if item[key] not in exist_urls]

        # insert filtered_items
        sql = NewFeedContract.SQL_INSERT
        self._insert_(sql, filtered_items, many=True)
        self.log.info("insert %d items success" % len(filtered_items))
        return len(filtered_items)

    def insert_website(self, items):
        # get insert site name, category
        query_items = []
        for item in items:
            query_items += [{WebSiteContract.PH_SITE_NAME: item[WebSiteContract.PH_SITE_NAME],
                             WebSiteContract.PH_CATEGORY: item[WebSiteContract.PH_CATEGORY]}]

        # get filtered items
        filtered_items = []
        for item in items:
            site_name = item[WebSiteContract.PH_SITE_NAME]
            category = item[WebSiteContract.PH_CATEGORY]
            rows = self.query_website_by_site_name_and_category(site_name, category).fetchall()
            if len(rows) == 0:
                filtered_items += [item]

        # insert filtered_items
        sql = WebSiteContract.SQL_INSERT
        self._insert_(sql, filtered_items, many=True)
        self.log.info("insert %d items success" % len(filtered_items))
        return len(filtered_items)

    # update
    def update_new_feed_is_check(self, ids, value):
        sql = NewFeedContract.SQL_UPDATE_IS_CHECK
        params = []
        for id_ in ids:
            params += [{
                NewFeedContract.PH_ID: id_,
                NewFeedContract.PH_IS_CHECKED: value
            }]

        ret = self._update_(sql, params, many=True)
        self.log.info("query_uncheck_item success")
        return ret

    # todo test
    def update_website_(self, ids, value):
        pass

    # delete
    def delete_new_feed(self, ids):
        sql = NewFeedContract.SQL_DELETE
        param = []
        for id_ in ids:
            param += [{NewFeedContract.PH_ID: id_}]

        self._delete_(sql, param, many=True)
        self.log.info("%s delete %d" % (NewFeedContract.TABLE_NAME, len(ids)))

    def delete_website(self, ids):
        sql = WebSiteContract.SQL_DELETE
        param = []
        for id_ in ids:
            param += [{WebSiteContract.PH_ID: id_}]

        self._delete_(sql, param, many=True)
        self.log.info("%s delete %d" % (WebSiteContract.TABLE_NAME, len(ids)))

    # query
    def query_website(self, limit=-1):
        sql = WebSiteContract.SQL_QUERY
        params = {}

        if limit != -1:
            sql = " ".join([sql, WebSiteContract.SQL_LIMIT])
            params[WebSiteContract.PH_LIMIT_NUMBER] = limit

        ret = self._query_(sql, params)
        self.log.info("query_all success")
        return ret

    def query_website_by_site_name_and_category(self, site_name, category, limit=-1):
        sql = WebSiteContract.SQL_QUERY_BY_SITE_NAME_AND_CATEGORY
        param = {WebSiteContract.PH_SITE_NAME: site_name,
                 WebSiteContract.PH_CATEGORY: category}

        if limit != -1:
            sql = " ".join([sql, WebSiteContract.SQL_LIMIT])
            param[WebSiteContract.PH_LIMIT_NUMBER] = limit

        ret = self._query_(sql, param)
        self.log.info("query_website_by_site_name_and_category")
        return ret

    def query_new_feed(self, limit=-1):
        sql = NewFeedContract.SQL_QUERY

        param = {}
        if limit != -1:
            sql = " ".join([sql, NewFeedContract.SQL_LIMIT])
            param[NewFeedContract.PH_LIMIT_NUMBER] = limit

        ret = self._query_(sql, param)
        self.log.info("query_all success")
        return ret

    def query_new_feed_by_urls(self, urls, limit=-1):
        # TODO hack
        # build sql
        ph = NewFeedContract.PH_IS_CHECKED
        str_wph = ','.join([':' + ph + str(i) for i in range(len(urls))])
        sql = NewFeedContract.SQL_QUERY_BY_URL % str_wph

        # build params
        ph_list = [ph + str(i) for i in range(len(urls))]
        params = {ph: url for ph, url in zip(ph_list, urls)}

        # add limit
        if limit != -1:
            sql = " ".join([sql, NewFeedContract.SQL_LIMIT])
            params[NewFeedContract.PH_LIMIT_NUMBER] = limit

        ret = self._query_(sql, params)
        self.log.info("%s query_by_urls success" % NewFeedContract.TABLE_NAME)
        return ret

    def query_new_feed_by_is_checked(self, value, limit=-1):
        sql = NewFeedContract.SQL_QUERY_BY_IS_CHECKED
        params = {NewFeedContract.PH_IS_CHECKED: value}

        if limit != -1:
            sql = " ".join([sql, NewFeedContract.SQL_LIMIT])
            params[NewFeedContract.PH_LIMIT_NUMBER] = limit

        ret = self._query_(sql, params)
        self.log.info("query_by_is_checked success")
        return ret

    def query_tables(self):
        sql = "SELECT name FROM SQLITE_MASTER WHERE TYPE='table'"
        rows = self._query_(sql, None).fetchall()
        return [row[0] for row in rows]

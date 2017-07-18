from main.DbHelper import DbHelper
from main.Parser import Parser
from main.DbContract import DBContract


class TestDbHelper(object):
    URL_SITE = """http://bbs.ruliweb.com/best/humor?&page=%d"""

    # def test_02_insert_items(self):
    #     parser = Parser()
    #
    #     items = []
    #     for i in range(1, 2 + 1):
    #         res = parser.parse_ruliweb(self.URL_SITE % i)
    #         items += res
    #
    #     db_helper = DbHelper()
    #     db_contract = DBContract()
    #     table_name = db_contract.TABLE_NAME_LIST[0]
    #
    #     res = db_helper.insert_items(table_name, items)
    #     assert (res is True, "insert fail")

    # TODO implement
    def setup_func(self):
        "set up test fixtures"
        pass

    # TODO implement
    def teardown_func(self):
        "tear down test fixtures"
        pass

    def test_00__init__(self):
        DbHelper()

    def test_01_query_all(self):
        parser = Parser()

        items = []
        for i in range(1, 2 + 1):
            res = parser.parse_ruliweb(self.URL_SITE % i)
            items += res

        db_helper = DbHelper()
        db_contract = DBContract()
        table_name = db_contract.TABLE_NAME_LIST[0]

        res = db_helper.insert_items(table_name, items)
        assert (res is True, "insert fail")

        rows = db_helper.query_all(table_name)
        assert (rows is not None, "query all fail")

        # if rows is not None:
        #     for i in rows:
        #         print(i)

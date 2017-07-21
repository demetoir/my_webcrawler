from main.DbContract import NewFeedContract
from main.DbHelper import DbHelper
from main.Interface import URL_SITE
from main.Parser import Parser

if __name__ == '__main__':

    parser = Parser()

    items = []
    for i in range(1, 2 + 1):
        res = parser.parse_ruliweb(URL_SITE % i)
        items += res

    items.sort(key=lambda item: item[NewFeedContract.KW_URL])

    db_helper = DbHelper()
    table_name = NewFeedContract.TABLE_NAME

    res = db_helper.insert_items(table_name, items)

    rows = db_helper.query_all(table_name)
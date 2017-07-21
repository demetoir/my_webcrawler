from main.DbContract import NewFeedContract
from main.Parser import Parser
from main import util

URL_SITE = """http://bbs.ruliweb.com/best/humor?&page=%d"""


def setup_func():
    pass


def teardown_func():
    pass


def test_01_parse_ruliweb():
    parser = Parser()

    ret = []
    for i in range(1, 4):
        ret += parser.parse_ruliweb(URL_SITE % i)

    ret.sort(key=lambda item: item[NewFeedContract.KW_URL])

    util.print_table(ret)

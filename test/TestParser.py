from nose import with_setup

from main.DbContract import NewFeedContract
from main.Parser import Parser
from main import util
from main.Tag import Tag

URL_SITE = """http://bbs.ruliweb.com/best/humor?&page=%d"""


def setup_func():
    pass


def teardown_func():
    pass


@with_setup(setup_func, teardown_func)
def test_00_setup():
    return


@with_setup(setup_func, teardown_func)
def test_99_teardown():
    return


@with_setup(setup_func, teardown_func)
def test_01_parse_ruliweb():
    parser = Parser()

    ret = []
    for i in range(1, 4):
        ret += parser.parse_ruliweb(URL_SITE % i)

    ret.sort(key=lambda item: item[NewFeedContract.PH_URL])

    util.print_rows(ret)

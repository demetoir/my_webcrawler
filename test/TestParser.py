import requests
from nose import with_setup

from main.DbContract import NewFeedContract
from main.Parser import Parser
from main import util

import webbrowser
import os

# from main.Tag import Tag

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


@with_setup(setup_func, teardown_func)
def test_02_parse_marumaru():
    parser = Parser()

    # page_num = 1
    # target_url = 'http://marumaru.in/?m=bbs&bid=mangaup&p=%d' % page_num

    target_url = 'http://www.schoolmusic.co.kr/Shop/index.php3?var=new_goods'
    ret = parser.parse_marumaru(target_url)

    # for i in ret:
    #     print(i)


@with_setup(setup_func, teardown_func)
def test_03_text_analizer():
    parser = Parser()
    target_url = 'http://marumaru.in/?m=bbs&bid=mangaup&p=1'
    url = 'http://bbs.ruliweb.com/best/humor'

    target_url = url

    html = parser.html_pruning(target_url)
    path = os.path.curdir
    file_name = 'punning_html.html'

    full_path = os.path.join(path, file_name)
    print(full_path)
    with open(full_path, 'wb') as f:
        f.write(html.encode('utf-8'))

    webbrowser.open_new_tab(full_path)

    # print(text)
    # ret = parser.html_analyzer(text)
    pass


def test_04_html_explorer():
    parser = Parser()
    url = 'http://bbs.ruliweb.com/best/humor'

    html = parser.get_html_text(url)

    parser.html_explorer(html)
    pass

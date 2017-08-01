from nose import with_setup

from main.Parser import Parser
from main import util
from main.htmlExplorer import HtmlExplorer

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
def test_01_init():
    parser = Parser()
    url = 'http://bbs.ruliweb.com/best/humor'
    html = parser.get_html_text(url)

    targets = ['head', 'script', 'header', 'footer', 'noscript']
    html = parser.html_delete_targets(html, targets)
    print(html)
    exp = HtmlExplorer(html)

    while True:
        util.open_web(str(exp.get_top()))

        for idx, child in enumerate(exp.contents()):
            if child.name is not None:
                print(idx, child.name, child.attrs)

        s = str(input())

        if s.isnumeric():
            exp.down(int(s))
        elif s is 'b':
            exp.up()
        else:
            break

    for name, attrs in exp.trace():
        print(name, attrs)

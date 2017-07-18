from main.Parser import Parser


class TestParser(object):
    URL_SITE = """http://bbs.ruliweb.com/best/humor?&page=%d"""

    def test_parser(self):

        parser = Parser()

        l = []
        for i in range(1, 2):
            res = parser.parse_ruliweb(self.URL_SITE % i)
            l += res

        for i in l:
            print(i)

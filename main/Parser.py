import requests
from bs4 import BeautifulSoup as bs

from main.DbContract import *
from main.logger import Logger
from main.Tag import Tag
HTML_PARSER = 'lxml'


class Parser(object):
    def __init__(self):
        self.log = Logger(self.__class__.__name__).log
        pass

    def parse_ruliweb(self, url):
        try:
            soup = bs(requests.get(url).text, HTML_PARSER)

            title_list = []
            url_list = []
            for page in soup.find_all(Tag.TAG_A):
                url_ = page.get(Tag.ATTR_HREF)
                title_ = page.string
                if url_ is not None and 'best/board/' in page.get(Tag.ATTR_HREF) \
                        and '유머 게시판' not in title_:
                    title_list += [title_]
                    url_list += [url_]

            ret = []

            for url_, title in zip(url_list, title_list):
                ret += [{NewFeedContract.PH_TITLE: title, NewFeedContract.PH_URL: url_}]

            self.log.info('parse success url = %s' % url)

        except Exception as e:
            self.log.error('parse error url = %s' % url)
            self.log.error(e)
            raise e

        return ret

    @staticmethod
    def parse_int(string):
        return "".join(filter(lambda c: chr(ord(c)).isnumeric(), string))

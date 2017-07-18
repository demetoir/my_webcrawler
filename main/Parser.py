import requests
from bs4 import BeautifulSoup as bs

from main.Tag import Tag
from main.DbContract import DBContract

HTML_PARSER = 'lxml'


class Parser(object):
    def __init__(self):
        pass

    def parse_ruliweb(self, url):
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
            ret += [{DBContract.PLACEHOLDER_TITLE: title, DBContract.PLACEHOLDER_URL: url_}]
        return ret

    @staticmethod
    def parse_int(string):
        return "".join(filter(lambda x: chr(ord(x)).isnumeric(), string))

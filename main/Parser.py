import requests
from bs4 import BeautifulSoup as bs, Comment

from main.DbContract import *
from main.logger import Logger
from main.Tag import Tag

HTML_PARSER = 'lxml'


class Parser(object):
    def __init__(self):
        self.log = Logger(self.__class__.__name__).log
        pass

    # hard coding parsing ruliweb
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

    def html_analyzer(self, html):
        # print(html)
        html = ' '.join(str(html).split())
        # print(html)

        tag_list = ['style', 'br', 'script', 'meta', 'button', 'head', 'body', 'html']
        soup = bs(html, HTML_PARSER)
        for item in soup.findChildren():
            if item.name in tag_list or len(item.contents) == 0:
                continue

            print(item.name)
            print(item.attrs)
            for idx, content in enumerate(item.contents):
                if str(content).isspace():
                    continue

                if len(str(content)) > 60:
                    print(idx, str(content)[:60] + '...')
                else:
                    print(idx, str(content))
            print('----------------------------------------------------------------')

    def get_html_text(self, url):
        return requests.get(url).text

    # html delete not using tag
    def html_delete_targets(self, html, targets):
        soup = bs(html, HTML_PARSER)
        # extract targets
        for target in targets:
            for item in soup.findAll(target):
                item.extract()

        # extract comment
        for item in soup.findAll(text=lambda text: isinstance(text, Comment)):
            item.extract()

        return str(soup)

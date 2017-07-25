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

    def parse_marumaru(self, target_url):

        ret = []
        try:
            soup = bs(requests.get(target_url).text, HTML_PARSER)

            # title_list = []
            # url_list = []
            ret = soup.find_all('a')

            pass
        except Exception as e:
            self.log.error('parse error url = %s' % target_url)
            self.log.error(e)
            raise e
        else:
            return ret

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

    def f(self, soup):
        print(soup)

    def get_html_text(self, url):
        return requests.get(url).text

    def html_pruning(self, url):
        html = requests.get(url).text
        html = ' '.join(html.split())
        soup = bs(html, HTML_PARSER)

        # extract comment
        for item in soup.findAll(text=lambda text: isinstance(text, Comment)):
            item.extract()

        # extract tag
        extract_tag_list = ['head', 'script', 'header', 'footer', 'noscript']
        for tag in extract_tag_list:
            [item.extract() for item in soup.find_all(tag)]

        # extract tag, attrs
        extract_tag_and_attrs = [('div', {'id': 'popup'}),
                                 ('div', {'class': 'notice_wrapper'}),
                                 ('div', {'id': 'context_menu'}),
                                 ('aside', {'class': 'aside_best'}),

                                 ('div', {'id': 'image_layer'})]
        for tag, attrs in extract_tag_and_attrs:
            for item in soup.find_all(tag, attrs):
                item.extract()

        soup = soup.html.body.div
        print(soup.children)
        print(soup.name)
        print(soup.attrs)
        for idx, content in enumerate(soup.contents):
            if str(content).isspace():
                continue

            if len(str(content)) > 60:
                print(idx, str(content)[:60] + '...')
            else:
                print(idx, str(content))

        # print(soup)
        return str(soup)

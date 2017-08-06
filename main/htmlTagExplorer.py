try:
    from bs4 import BeautifulSoup as bs
    from main.Parser import HTML_PARSER

except ModuleNotFoundError as e:
    from Parser import HTML_PARSER


class HtmlTagExplorer(object):
    def __init__(self, html=None):
        if html is not None:
            self.__root__ = bs(html, HTML_PARSER)
            self.__stack__ = [self.__root__]

    def __repr__(self):
        return self.__class__.__name__

    def __len__(self):
        return len(self.__stack__)

    def __root__(self, html):
        self.__root__ = bs(html, HTML_PARSER)
        self.__stack__ = [self.__root__]

    def down(self, idx):
        top = self.__stack__[-1]
        if top.contents[idx].name is not None:
            self.__stack__ += [top.contents[idx]]

    def up(self, ):
        if len(self.__stack__) != 1:
            self.__stack__.pop()

    def contents(self):
        return self.__stack__[-1].contents

    def trace_stack(self):
        trace = []
        for item in self.__stack__[1:]:
            cur = self.__root__.find(item.name, item.attrs)
            trace += [(cur.name, cur.attrs)]
        return trace

    def top(self):
        return self.__stack__[-1]

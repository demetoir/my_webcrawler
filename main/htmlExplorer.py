from bs4 import BeautifulSoup as bs
from main.Parser import HTML_PARSER


class HtmlExplorer(object):
    def __init__(self, html):
        self.root = bs(html, HTML_PARSER)
        self.stack = [self.root]

        pass

    def down(self, idx):
        top = self.stack[-1]
        if top.contents[idx].name is not None:
            self.stack += [top.contents[idx]]

    def up(self, ):
        self.stack.pop()

    def contents(self):
        return self.stack[-1].contents

    def trace(self):
        trace = []
        for item in self.stack[1:]:
            cur = self.root.find(item.name, item.attrs)
            trace += [(cur.name, cur.attrs)]
        return trace

    def get_top(self):
        return self.stack[-1]

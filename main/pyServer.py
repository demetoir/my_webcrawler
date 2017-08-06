import zerorpc
from os import path
try:
    from main.logger import Logger
    from main.htmlTagExplorer import HtmlTagExplorer as txp
except ModuleNotFoundError as e:
    from htmlTagExplorer import HtmlTagExplorer as txp
    from logger import Logger
    # from htmlTagExplorer import HtmlTagExplorer as txp
    # from logger import Logger

class pyServer():
    def __init__(self):
        self.log = Logger(self.__class__.__name__).log
        self.txp = txp()
        pass

    def __repr__(self):
        return self.__class__.__name__

    def echo(self, text):
        """echo any text"""
        self.log.info(text)
        return text

    def f(self, text, num, ):
        return "response %s %d" % (text, int(num))

    def set_target_address(self, address):
        self.txp.__root__(address)
        return "address set"


def main():
    port = str(4242)
    addr = 'tcp://127.0.0.1:' + port
    server = zerorpc.Server(pyServer())
    server.bind(addr)
    print('start running on {}'.format(addr))

    try:
        server.run()
    except Exception as e:
        pass


if __name__ == '__main__':
    main()

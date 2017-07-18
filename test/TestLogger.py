from main.logger import Logger


class TestLogger(object):
    def test_logger(self):
        log1 = Logger("111").log

        log2 = Logger("222").log

        log1.debug("log1 debug")

        log2.debug("log2 debug")

        pass

from nose import with_setup

from main.logger import Logger


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
def test_01_logger():
    log1 = Logger("111").log
    log2 = Logger("222").log

    log1.debug("log1 debug")
    log2.debug("log2 debug")



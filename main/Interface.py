# import time
# import random
#
# class Delay(object):
#     def __init__(self):
#         self.time = 1
#         pass
#
#     def delay(self):
#         time.sleep(self.time + float(random.randint(1000)) / 1000)

class Interface(object):
    def __init__(self):
        pass

    def init_db(self):
        pass

    def update_db(self):
        pass

    def get_new_feed(self):
        pass

    def get_website(self):
        pass

    def delete_feed(self):
        pass

    def check_feed(self):
        pass


URL_SITE = """http://bbs.ruliweb.com/best/humor?&page=%d"""

if __name__ == '__main__':
    # parser = CrawlerParser()
    # # delay = Delay()
    # dbHelper = CrawlerDbHelper()
    #
    # l = []
    # for i in range(1, 5):
    #     res = parser.ruliweb_parser(URL_SITE % i)
    #     # delay.delay()
    #     l += res
    #
    #
    # for i in l:
    #     print(i)
    pass

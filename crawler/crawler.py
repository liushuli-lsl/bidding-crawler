from .searching import BiddingSearching
from .parseing import BiddingParseing
from .exceptions import (ForbiddenError, ServiceUnavailableError)

import queue as mq
import threading
import time

queueLock = threading.Lock()

"""
BiddingCrawler 负责爬虫行为的控制，相当于 scrapy 的引擎
"""
class BiddingCrawler(threading.Thread):

    def __init__(self, name, page_index, queue):
        threading.Thread.__init__(self)
        # 线程名称，暂时无用
        self.name = name

        # 要搜索的页数的索引
        self.page_index = page_index

        # 搜索器对象，执行采购公告的所有
        self.searcher = BiddingSearching()

        # 解析器对象，解析获取到的 html 页面
        self.parser = BiddingParseing()

        self.queue = queue


    def run(self):
        biddings = self.get_biddings(self.page_index)

        queueLock.acquire()

        for b in biddings:
            self.queue.put(b)

        queueLock.release()

        time.sleep(1)
    
    def get_biddings(self, page_index):
        return self.parser.parse(self.searcher.search(page_index))
        


if __name__ == "__main__":
    pass

# -*- coding: utf-8 -*-
from .searching import BiddingSearching
from .parseing import PageParseing
from .crawler import BiddingCrawler
from .storing import BiddingStoring
from .exceptions import (ForbiddenError, ServiceUnavailableError)
from .setting import PAGE_WAIT_INTERVAL,MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

import queue
import logging
import logging.config
import threading
import time
import sys
from os import path
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
import pymysql

log_file_path = path.join(path.dirname(path.abspath(__package__)), 'conf/logging.conf')

logging.config.fileConfig(log_file_path)
logger = logging.getLogger('main.scheduler')


class CrawlerScheduler(threading.Thread):
    """
    CrawlerSchduler 负责爬虫的调度
    
    由于每次调度都可能会产生抓取和入库，在这期间可能会有新的采购公告产生，可能会导致数据漏爬，
    为了解决这个问题，每天晚上 11 点，都会对当天产生的公告进行一次统一抓取。

    """
    
    def __init__(self, number, work_queue):
        threading.Thread.__init__(self)

        self.number = number  # 线程编号

        self.work_queue = work_queue

        self.searcher = None
        self.stored = None
        self.page_parser = None


    def _crawler_progress(self, current, max_size):
        """
        页面采集进度条，用于显示页面采集进度
        """
        sys.stdout.write("  已解析页面:%.2f%%" % float(current / max_size) + '\r')
        sys.stdout.flush()

    def _reload_last_processed(self):
        """
        重新加载上一次任务执行后的处理结果
        """
        self.searcher = BiddingSearching()
        self.stored = BiddingStoring(work_queue)
        self.page_parser = PageParseing()

    def run(self):

        self._reload_last_processed()

        logger.info('开始任务启动的数据采集。')

        page_size = self.page_parser.parse(self.searcher.search())
        additional_record_size = self.page_parser.additional_record_size
        logger.info('本次采集将要获取 {} 条采购公告，分为 {} 页。'.format(additional_record_size, page_size))

        # 2 秒后再开始数据采集，防止速度过快导致 403
        time.sleep(2)

        is_success = False

        for i in range(page_size):
            page_index = i + 1
            # 不使用多线程，http://www.ccgp.gov.cn/ 可能有爬虫识别，过快的抓取会导致页面 403
            t = BiddingCrawler('t' + str(page_index), page_index, self.work_queue)

            try:
                biddings = t.get_biddings(page_index)

                for b in biddings:
                    self.work_queue.put(b)

                self._crawler_progress(page_index, page_size)

                # 等待 2 秒，降低搜索频率，防止被网站认为是爬虫
                time.sleep(PAGE_WAIT_INTERVAL)
            except (ForbiddenError, ServiceUnavailableError) as err:
                logger.error("Search error: {0}".format(err))
                time.sleep(1)
                # 一旦发生这类错误，下次再采集
                break
            except Exception as err:
                logger.error("Unknow error: {0} type {1}".format(err, type(err)))
                # 一旦发生这类错误，下次再采集
                break

        logger.info('页面采集完成，本次采集公告 {} 条。'.format(work_queue.qsize()))

        logger.info('开始存储采集公告。')
        self.stored.stored()
        logger.info('公告存储完成。')



app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    conn = pymysql.connect(host = MYSQL_HOST, port = MYSQL_PORT, user = MYSQL_USER, password = MYSQL_PASSWORD, db = MYSQL_DB)
    cur = conn.cursor()
    sql = "SELECT * FROM bidding_index"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    pub_time= []
    for row in u:
        pub_time.append(row[4])

    print("生成数据",min(pub_time),max(pub_time))
    total = len(list(u))
    print("生成数据长度",total)
    data={"min_pub_time":min(pub_time),
          "max_pub_time":max(pub_time),
          "total":total,
          "u":u}
    return render_template('index.html',data=data)


if __name__ == "__main__":

    logger.info('Crawler Scheduler Startup...')

    req_thread = []
    work_queue = queue.Queue(0)

    t = CrawlerScheduler(1, work_queue)
    t.start()

    req_thread.append(t)

    for t in req_thread:
        t.join()
    
    logger.info('Crawler Scheduler End.')
    app.run()


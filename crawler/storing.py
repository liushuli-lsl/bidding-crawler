# -*- coding: utf-8 -*-
from configparser import ConfigParser
from os import path
from .setting import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

import pymysql
import queue
import logging
import threading
import time

logger = logging.getLogger('main.storing')

"""
log_file_path = path.join(path.dirname(path.abspath(__package__)), 'conf/mysql.conf')

parser = ConfigParser()
parser.read(log_file_path)

host = parser.get('mysql', 'db_host')
port = parser.get('mysql', 'db_port')
user = parser.get('mysql', 'db_user')
password = parser.get('mysql', 'db_password')
database = parser.get('mysql', 'db_database')
"""


class BiddingStoring(threading.Thread):

    def __init__(self, work_queue):
        threading.Thread.__init__(self)

        # 用来保证获取的采购公告不重复
        self.bidding_cache = {}

        self.work_queue = work_queue


    def run(self):
        while True:
            self.stored()

            # 休息 30 秒
            time.sleep(30)


    def _is_processed(self, content_link):
        return self.bidding_cache.get(hash(content_link), None) != None


    def _put_to_bidding_cache(self, content_link):
        self.bidding_cache[hash(content_link)] = True


    def reload_bidding_cache(self):
        """
        从数据库中重新加载重复公告检查器
        """

        # 打开数据库连接
        db = pymysql.connect(host = MYSQL_HOST, port = MYSQL_PORT, user = MYSQL_USER, password = MYSQL_PASSWORD, db = MYSQL_DB)

        record_size = 0
        try:
            with db.cursor() as cursor:
                sql = 'select link from bidding_index where date_format(pub_time, \'%y-%m-%d\') = date_format(now(), \'%y-%m-%d\')'

                logger.info(sql)
                try:
                    # 重置缓存 TODO: 缺少每日重置的处理
                    self.bidding_cache = {}

                    # 执行sql语句
                    cursor.execute(sql)
                    # 获取所有记录列表
                    results = cursor.fetchall()
                    for row in results:
                        # 已经处理过的要添加到列表中，放置后续重复处理
                        self._put_to_bidding_cache(row[0])
                        record_size += 1
                except:
                    logger.error('执行 SQL语句 [%s] 时发生错误。' % sql)
        finally:
            db.close()
        
        return record_size


    def stored(self):

        # 打开数据库连接
        db = pymysql.connect(host = MYSQL_HOST, port = MYSQL_PORT, user = MYSQL_USER, password = MYSQL_PASSWORD, db = MYSQL_DB)
        
        stored_count = 0

        try:
            with db.cursor() as cursor:
                while not self.work_queue.empty():
                    bidding = self.work_queue.get()
                    
                    # 字典中存在，则说明已经处理过
                    # hash 是为了减少内存占用
                    if self._is_processed(bidding.content_link):
                        logger.debug('采购公告 {}, 重复，URL: {}'.format(bidding.name, bidding.content_link))
                        continue

                    sql = "INSERT INTO `source`.`bidding_index`(`name`, `link`, `type`, `pub_time`, `zone`, `buyer_name`, `agent_name`) \
                            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(bidding.name, bidding.content_link, bidding.type, bidding.pub_time, \
                                bidding.zone, bidding.buyer_name, bidding.agent_name)
                    try:
                        # 执行sql语句
                        cursor.execute(sql)
                        # 提交到数据库执行
                        db.commit()
                        # 已经处理过的要添加到列表中，放置后续重复处理
                        self._put_to_bidding_cache(bidding.content_link)
                        stored_count += 1
                    except:
                        logger.error('执行 SQL语句 [%s] 时发生错误。' % sql)

        finally:
            logger.info('本次采集任务共入库 %s 条采购公告。' % stored_count)
            db.close()
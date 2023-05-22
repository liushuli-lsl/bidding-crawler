from .run import CrawlerScheduler

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

import os
import queue

def job():

    req_thread = []
    work_queue = queue.Queue(0)

    t = CrawlerScheduler(1, work_queue)
    t.run()

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # 周一至周五，每天晚上 10：30 执行任务
    scheduler.add_job(job, 'cron', day_of_week='1-5', hour=22, minute=30)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
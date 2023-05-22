# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import NavigableString
from typing import List

from .models import Bidding
from .utils import (
    get_pub_time_from_content, 
    get_agent_from_content, 
    get_buyer_from_content, 
    get_max_record_from_content
)
from math import *
import re
import logging

logger = logging.getLogger('main.parseing')

"""
采购公告解析器
根据给定的条件，搜索采购公告
"""
class BiddingParseing(object):

    def __init__(self):
        pass

    """
    解析 HTML 页面中的采购公告，并生成 Bidding 对象

    Args:
        text: 抓取到的网页

    Return:
        返回解析生成的 Bidding 列表

    :rtype: crawler.Bidding
    """
    def parse(self, text) -> List[Bidding]:

        if text == None:
            return None
    
        resp_html = BeautifulSoup(text, "lxml")

        results_ul = resp_html.find_all('ul', class_ = 'vT-srch-result-list-bid')
        results_li = results_ul[0].select('li') # 查找所有的 li 标签，css 选择器返回的也是 ResultSet 对象

        biddings = []

        for li_tag in results_li:
            bidding = Bidding()
            
            bidding.name = li_tag.a.string.strip()
            bidding.content_link = li_tag.a.get('href')
            bidding.type = li_tag.span.strong.string.strip()
            bidding.pub_time = get_pub_time_from_content(li_tag.span.text)
            bidding.buyer_name = get_buyer_from_content(li_tag.span.text)
            bidding.agent_name = get_buyer_from_content(li_tag.span.text)
            bidding.zone = self._get_zone_from_content(li_tag.span.a.string)

            biddings.append(bidding)

        return biddings
    
    def _get_zone_from_content(self, zone):
        return zone.strip() if type(zone) == NavigableString and zone != '' else None


"""
解析检索到的页面中总的公告条数，该值可用于确定分页数，并结合上一次检索结果计算本次需要检索的公告条数
"""
class PageParseing(object):

    def __init__(self):
        # 每页最大显示记录数
        self._MAX_PAGE_RECORD_NUMBERS = 20
        # 本次检索总条数
        self.max_record_size = 0
        # 本次检索的有效记录条数。有效记录指的是没有抓取过的记录：本次检索总条数 - 上次检索总条数 = 本次检索有效记录数
        self.additional_record_size = 0
        # 本次检索的有效页数 = 本次检索有效记录数 / 每页最大显示记录数
        self.page_size = 0
        # 上次检索总条数
        self.last_processed_record_size = 0

    def parse(self, text) ->int:
        if text == None:
            return None

        resp_html = BeautifulSoup(text, "lxml")

        # 查找分页部分
        results = resp_html.find_all('p', style = 'float:left')

        try:
            # 获取本次抓取采集到的最大记录数
            self.max_record_size = self._get_record_size(results[0].text)
        except IndexError as err:
            logger.error('list index out of range, html: %s' % text)
            raise

        logger.info('max_record_size: %s' % self.max_record_size)
        logger.info('last_processed_record_size: %s' % self.last_processed_record_size)

        self.additional_record_size = self.max_record_size - self.last_processed_record_size
        self.page_size = ceil(self.additional_record_size / self._MAX_PAGE_RECORD_NUMBERS)

        logger.info('additional_record_size: %s' % self.additional_record_size)

        return self.page_size

    """
    获取本次检索时的总记录数

    Args:
        text: 关于总记录数的描述，一般为如下内容：'关键字：标题检索共找到100条内容查询日期从2020-08-27到2020-08-27'

    Return:
        返回本次查询总的记录数
    """
    def _get_record_size(self, text):
        return int(get_max_record_from_content(self._cleanup_text(text)))

    def _cleanup_text(self, text):
        return text.replace('\r\n', '').replace('\n', '').replace(' ', '')



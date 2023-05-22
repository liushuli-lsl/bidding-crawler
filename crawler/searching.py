from .exceptions import (ForbiddenError, ServiceUnavailableError)
from .models import SearchArgument

import requests


class BiddingSearching(object):
    """
    采购公告搜索器
    根据给定的条件，搜索采购公告
    """

    def __init__(self):
        self.search_argument = SearchArgument()

        # 返回的网页编码
        self.encoding = 'UTF-8'


    """
    获取本次检索时的总记录数

    Args:
        index: 当前搜索的页数，默认值为 1

    Return:
        返回本次搜索抓取到的网页，字符串类型

    Raise:
        ForbiddenError

        ForbiddenError
    """
    def search(self, index: int = 1):
        self.search_argument.page_index = index
        payload = self.search_argument.prepare_arguments()

        # 必须要有 user-agent，模拟浏览器访问，否则会返回 403。
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

        resp = requests.get(self.search_argument.server, params = payload, headers = headers)
        resp.encoding = self.encoding

        if resp.status_code == 403:
            raise ForbiddenError("访问 URL: [%s] 被禁止，HTTP 状态码为: %s" % (resp.url, resp.status_code))
        elif resp.status_code == 503:
            raise ServiceUnavailableError("URL: [%s] 服务暂不可用，HTTP 状态码为: %s" % (resp.url, resp.status_code))

        # 这个网站在请求繁忙时，还需要输入验证码

        # 返回抓取到的 html 页面
        return str(resp.text)
    



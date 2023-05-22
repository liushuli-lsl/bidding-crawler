
class Bidding(object):
    """
    采购公告模型
    """
    
    def __init__(self):
        #: 采购公告的名称
        self.name = None

        #: 采购公告详细内容的链接
        self.content_link = None

        #: 公告类型，默认为所有类型。
        #: 1 公开招标，2 询价公告，3 竞争性谈判，4 单一来源，5 资格预审，6 邀请公告，7 中标公告，
        #: 8 更正公告，9 其他公告，10 竞争性磋商，11 成交公告，12 废标终止
        self.type = None

        #: 公告发布时间
        self.pub_time = None

        #: 公告发布地区（省、自治区、直辖市）的简称
        self.zone = None

        #: 采购人名称
        self.buyer_name = None

        #: 代理机构名称
        self.agent_name = None

    def __str__(self):
        return "name:%s, content_link:%s, type:%s, pub_time:%s, zone:%s, buyer_name:%s, agent_name:%s" % (self.name, self.content_link, self.type, self.pub_time, self.zone, self.buyer_name, self.agent_name)



class SearchArgument(object):

    def __init__(self):
        self.server = 'http://search.ccgp.gov.cn/bxsearch'

        # 搜索类型。1 表示搜标题，2 表示搜全文。默认为 1 搜标题。
        self.search_type = '1'

        # 检索的页面，默认为 1
        self.page_index = 1

        # 公告类别，默认搜索"地方公告"。0 所有类别，1 中央公告，2 地方公告
        self.bid_sort = '2'

        # 按采购人名称搜索
        self.buyer_name = ''

        # 按项目编号搜索
        self.project_id = ''

        # 公告品目，默认为所有品目。0 所有品目，1 货物类，2 工程类，3 服务类
        self.pin_mu = '0'

        # 公告类型，默认为所有类型。
        # 1 公开招标，2 询价公告，3 竞争性谈判，4 单一来源，5 资格预审，6 邀请公告，7 中标公告，
        # 8 更正公告，9 其他公告，10 竞争性磋商，11 成交公告，12 废标终止
        self.bid_type = '0'

        self.db_select = 'bidx'

        # 不太清楚这个参数的含义
        self.kw = ''

        # 查询开始时间，时间格式为 yyyy:MM:dd，:在 html 中需替换为 %3A
        self.start_time = ''

        # 查询结束时间，时间格式为 yyyy:MM:dd，:在 html 中需替换为 %3A
        self.end_time = ''

        # 时间类型
        # ['0':'今天', '1':'近3日', '2':'近1周', '3':'近1周', '4':'近1月', '5':'近3月', '6':'近半年', '7':'指定时间']
        self.time_type = '0'

        # 地区（显示名称）
        self.display_zone = ''

        # 地区Id
        self.zone_id = ''

        # 不会涉及这里项目
        self.ppp_status = ''

        # 代理机构
        self.agent_name = ''


    def prepare_arguments(self):
        """
        构造查询用的查询条件参数

        :rtype: dict
        """
        return {'searchtype': self.search_type
                , 'page_index': self.page_index
                , 'bidSort': self.bid_sort
                , 'buyerName': self.buyer_name
                , 'projectId': self.project_id
                , 'pinMu': self.pin_mu
                , 'bidType': self.bid_type
                , 'dbselect': self.db_select
                , 'kw': self.kw
                , 'start_time': self.start_time
                , 'end_time': self.end_time
                , 'timeType': self.time_type
                , 'displayZone': self.display_zone
                , 'zoneId': self.zone_id
                , 'pppStatus': self.ppp_status
                , 'agentName': self.agent_name}


# bidding-crawler

#### 介绍
招标信息爬虫
工作需要做一个爬取招标信息的工具。

#### 软件架构
0.0.1版本没什么架构，目前也只能爬取 http://www.ccgp.gov.cn/ 的采购公告，说一下各个文件的分工

1.  models.py 定义了招标公告数据模型和搜索参数数据模型
2.  searching.py 执行搜索，并返回搜索结果的 string 表示
3.  parseing.py 提供了两种解析，一种是解析此次搜索获得了多少条记录，并且分成多少页；另一种是解析单个页面的内容，并形成招标公告数据模型
4.  storeing.py 用于将 Bidding 模型写入数据库





#### 使用说明

1.  需要一个 MySQL 数据库，连接参数参见 setting.py
2.  执行时需要用：python -m crawler.run

#### 参与贡献

都是我自己弄得




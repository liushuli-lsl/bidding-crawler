from bs4 import BeautifulSoup

import re

def search(pattern, text):
    matched = re.search(pattern, text)
    return matched.group() if matched else None


def get_buyer_from_content(text):
    return search('((?<=采购人：)(.*))', text)


def get_agent_from_content(text):
    return search('((?<=代理机构：)(.*))', text)


def get_pub_time_from_content(text):
    pattern = '[1-9]\d{3}.(0[1-9]|1[0-2]).(0[1-9]|[1-2][0-9]|3[0-1]) (20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d'
    return search(pattern, text)


def get_max_record_from_content(text):
    result = search('((?<=标题检索共找到)(.*)(?=条内容))', text)
    return int(result) if result != None else 0

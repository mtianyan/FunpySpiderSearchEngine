# encoding: utf-8
from scrapy import Selector

__author__ = 'mtianyan'
__date__ = '2018/1/25 0025 21:26'
import requests

response = requests.get("https://www.aqistudy.cn/historydata/daydata.php?city=%E6%9C%AC%E6%BA%AA&month=201502")
sel = Selector(response)
list = sel.xpath("//tr").extract()[1:]
pass
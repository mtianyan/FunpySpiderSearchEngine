# _*_ coding: utf-8 _*_
__author__ = 'mtianyan'
__date__ = '2017/3/28 12:06'

import sys
import os
from scrapy.cmdline import execute

#将系统当前目录设置为项目根目录
#os.path.abspath(__file__)为当前文件所在绝对路径
#os.path.dirname为文件所在目录
# C:\Users\mtianyan\Desktop\ArticleSpider\main.py
# C:\Users\mtianyan\Desktop\ArticleSpider
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#执行命令，相当于在控制台cmd输入改名了
# execute(["scrapy", "crawl" , "jobbole"])
execute(["scrapy", "crawl" , "zhihu"])
# execute(["scrapy", "crawl" , "lagou"])
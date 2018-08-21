__author__ = 'mtianyan'
__date__ = '2018/8/20 04:34'

from scrapy.cmdline import execute

import sys
import os

"""
将项目根目录加入系统环境变量中国。
os.path.abspath(__file__)为当前文件所在绝对路径 .../FunpySpiderSearch/main.py
os.path.dirname() 获取文件的父目录  .../FunpySpiderSearch
"""
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

"""
调用execute函数执行scrapy命令，相当于在控制台cmd输入该命令
可以传递一个数组参数进来
"""
# execute(["scrapy", "crawl", "jobbole"])

# execute(["scrapy", "crawl", "lagou"])

execute(["scrapy", "crawl", "zhihu"])

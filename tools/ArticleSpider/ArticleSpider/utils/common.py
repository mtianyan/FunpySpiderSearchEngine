# _*_ coding: utf-8 _*_
import hashlib
import re

__author__ = 'mtianyan'
__date__ = '2017/5/22 20:56'

def get_md5(url):
    #str就是unicode了
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def extract_num(text):
    #从字符串中提取出数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

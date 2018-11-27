__author__ = 'mtianyan'
__date__ = '2018/8/20 07:40'

import datetime
import re


def str2date(value):
    """字符串转换时间方法"""
    try:
        value.strip().replace("·", "").strip()
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


def get_nums(value):
    """获取字符串内数字方法"""
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def return_value(value):
    """直接获取值方法"""
    return value


def exclude_none(value):
    """排除none值"""
    if value:
        return value
    else:
        value = "无"
        return value

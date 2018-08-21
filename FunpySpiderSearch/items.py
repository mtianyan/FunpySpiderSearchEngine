# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from abc import ABCMeta, abstractmethod


class FunpyspidersearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


"""
具体的items，请看sitems文件夹中的网站items
域名+内容+Item
"""


class BaseItem(metaclass=ABCMeta):
    """
    基础的每个Item都应该实现的接口
    """

    field_list = []  # 字段名

    # @abstractmethod
    # def field_define(self):
    #     """
    #     TODO: 定义Item应该具有的字段,暂时不会如何给类塞进去成员，未完待续。
    #     :return:
    #     """
    #     pass

    @abstractmethod
    def clean_data(self):
        """
        对于原始提取字段进行清理
        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def help_fields(fields: list):
        """
        帮助生成field定义字段代码。
        :param fields:
        :return:
        """
        pass


class MysqlItem(BaseItem):
    """
    数据存取至mysql数据库应该实现的接口
    """
    table_name = ""  # 数据库表名
    duplicate_key_update = []  # "重复插入时，需要更新的字段"

    @abstractmethod
    def save_to_mysql(self):
        """
        生成插入数据库的sql语句
        :return:
        """
        pass


class ElasticSearchItem(BaseItem):
    """
    数据存取至ElasticSearch应该实现的接口
    """

    @abstractmethod
    def save_to_es(self):
        """
        对于数据保存到es中
        :return:
        """
        pass

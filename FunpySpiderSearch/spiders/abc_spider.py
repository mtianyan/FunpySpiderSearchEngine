from abc import ABCMeta, abstractmethod

__author__ = 'mtianyan'
__date__ = '2018/8/21 01:27'


class MyBaseSpider(metaclass=ABCMeta):
    """
    基础的每个Spider都应该实现的接口,使用spider模板吧，不要重复造轮子。
    """

    # @abstractmethod
    # def login(self):
    #     """实现登录方法，如果无需登录，pass即可"""
    #     pass
    #
    # def parse_content(self):
    #     """解析具体单页内容的方法"""
    #     pass

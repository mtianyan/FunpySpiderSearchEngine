from abc import ABCMeta, abstractmethod

"""
具体的items，请看sites文件夹中的网站items
域名+内容+Item
"""


class BaseItem(metaclass=ABCMeta):
    """
    基础的每个Item都应该实现的接口
    """

    @abstractmethod
    def clean_data(self):
        """
        对于原始提取字段进行清理
        :return:
        """
        pass


class MysqlItem(BaseItem):
    """
    数据存取至mysql数据库应该实现的接口
    """

    @abstractmethod
    def save_to_mysql(self):
        """
        生成插入数据库的sql语句
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
        """
        pass

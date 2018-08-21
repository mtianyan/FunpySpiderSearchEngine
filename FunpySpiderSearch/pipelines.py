# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class FunpyspidersearchPipeline(object):
    @staticmethod
    def process_item(item, spider):
        return item


class MysqlTwistedPipeline(object):
    """
    通用的数据库保存Pipeline
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        自定义组件或扩展很有用的方法: 这个方法名字固定, 是会被scrapy调用的。
        这里传入的cls是指当前的class
        """
        db_parms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        # 连接池ConnectionPool
        dbpool = adbapi.ConnectionPool("MySQLdb", **db_parms)

        # 此处相当于实例化pipeline, 要在init中接收。
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将mysql插入变成异步执行
        参数1: 我们每个item中自定义一个函数,里面可以写我们的插入数据库的逻辑
        """
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 添加自己的处理异常的函数
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
        """
        执行具体的插入
        根据不同的item 构建不同的sql语句并插入到mysql中
        """
        insert_sql, params = item.save_to_mysql()
        cursor.execute(insert_sql, params)

    @staticmethod
    def handle_error(failure, item, spider):
        # 处理异步插入的异常
        print(failure)


class ElasticSearchPipeline(object):
    """通用的ELasticSearch存储方法"""

    def process_item(self, item, spider):
        item.save_to_es()
        return item

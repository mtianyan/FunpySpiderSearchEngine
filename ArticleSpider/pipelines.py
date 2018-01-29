# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from datetime import datetime
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from ArticleSpider.models.es_jobbole import ArticleType
from ArticleSpider.models.es_lagou import LagouType
from ArticleSpider.models.es_zhihu import ZhiHuQuestionType,ZhiHuAnswerType
from w3lib.html import remove_tags

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 异步操作mysql插入
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    # 自定义组件或扩展很有用的方法: 这个方法名字固定, 是会被scrapy调用的。
    # 这里传入的cls是指当前的MysqlTwistedPipline class
    def from_settings(cls, settings):
        # setting值可以当做字典来取值
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        # 连接池ConnectionPool
        # def __init__(self, dbapiName, *connargs, **connkw):
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        # 此处相当于实例化pipeline, 要在init中接收。
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行：参数1：我们自定义一个函数,里面可以写我们的插入逻辑
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 添加自己的处理异常的函数
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)


class MysqlPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect(
            '127.0.0.1',
            'root',
            'tp158917',
            'articlespider',
            charset="utf8",
            use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s)
        """
        # 使用VALUES实现传值
        self.cursor.execute(
            insert_sql,
            (item["title"],
             item["url"],
                item["create_date"],
                item["fav_nums"]))
        self.conn.commit()

# 自定义的将伯乐在线内容保存到本地json的pipeline


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        # 使用codecs打开避免一些编码问题。
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        # 将item转换为dict,然后调用dumps方法生成json对象，false避免中文出错
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    # 当spider关闭的时候: 这是一个spider_closed的信号量。
    def spider_closed(self, spider):
        self.file.close()


# 调用scrapy提供的json export导出json文件
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(
            self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# 自定义的pipeline,可实现下载图片的同时获取本地地址。
class ArticleImagePipeline(ImagesPipeline):
    # 重写该方法可从result中获取到图片的实际下载地址
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item

class ElasticSearchPipeline(object):
    # 将伯乐在线数据写入到es中
    def process_item(self, item, spider):
        # 将item转换为es数据。
        article = ArticleType()
        article.title = item["title"]
        article.create_date = item["create_date"]
        article.content = remove_tags(
            item["content"]).strip().replace(
            "\r\n",
            "").replace(
            "\t",
            "")
        article.front_image_url = item["front_image_url"]
        if "front_image_path" in item:
            article.front_image_path = item["front_image_path"]
        article.praise_nums = item["praise_nums"]
        article.comment_nums = item["comment_nums"]
        article.fav_nums = item["fav_nums"]
        article.url = item["url"]
        article.tags = item["tags"]
        article.id = item["url_object_id"]

        # title_suggest = self.gen_suggests(article.title, article.tags)
        # article.title_suggest = title_suggest

        article.save()
        return  item

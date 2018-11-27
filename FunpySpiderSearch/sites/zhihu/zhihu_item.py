__author__ = 'mtianyan'
__date__ = '2018/8/20 07:28'

import datetime

import scrapy
from elasticsearch_dsl import connections
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags

from FunpySpiderSearch.items import MysqlItem, ElasticSearchItem
from FunpySpiderSearch.settings import SQL_DATETIME_FORMAT
from FunpySpiderSearch.sites.zhihu.es_zhihu import ZhiHuQuestionIndex, ZhiHuAnswerIndex
from FunpySpiderSearch.utils.common import extract_num, extract_num_include_dot, real_time_count
from FunpySpiderSearch.utils.es_utils import generate_suggests
from FunpySpiderSearch.utils.mysql_utils import fun_sql_insert
from FunpySpiderSearch.utils.string_util import exclude_none

es_zhihu_question = connections.create_connection(ZhiHuQuestionIndex)
es_zhihu_answer = connections.create_connection(ZhiHuAnswerIndex)
ZHIHU_QUESTION_COUNT_INIT = 0
ZHIHU_ANSWER_COUNT_INIT = 0


class ZhihuQuestionItem(scrapy.Item, MysqlItem, ElasticSearchItem):
    url_object_id = scrapy.Field()
    question_id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field(
        input_processor=MapCompose(exclude_none),
    )
    topics = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()

    def clean_data(self):
        self["question_id"] = self["question_id"][0]
        self["topics"] = ",".join(self["topics"])
        self["url"] = self["url"][0]
        self["title"] = "".join(self["title"])
        try:
            self["content"] = "".join(self["content"])
            self["content"] = remove_tags(self["content"])
        except BaseException:
            self["content"] = "无"
        try:
            self["answer_num"] = extract_num("".join(self["answer_num"]))
        except BaseException:
            self["answer_num"] = 0
        self["comments_num"] = extract_num("".join(self["comments_num"]))

        if len(self["watch_user_num"]) == 2:
            watch_user_num_click = self["watch_user_num"]
            self["watch_user_num"] = extract_num_include_dot(watch_user_num_click[0])
            self["click_num"] = extract_num_include_dot(watch_user_num_click[1])
        else:
            watch_user_num_click = self["watch_user_num"]
            self["watch_user_num"] = extract_num_include_dot(watch_user_num_click[0])
            self["click_num"] = 0

        self["crawl_time"] = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

    def save_to_mysql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
                   insert into zhihu_question(url_object_id,question_id, title, content,topics,
                    answer_num, comments_num,watch_user_num, click_num, url,
                     crawl_time
                     )
                   VALUES (%s, %s, %s, %s, %s
                   , %s, %s, %s, %s, %s,
                   %s)
                   ON DUPLICATE KEY UPDATE
                   content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
                   watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
               """
        self.clean_data()
        sql_params = (
            self['url_object_id'], self["question_id"], self["title"], self["content"], self["topics"],
            self["answer_num"], self["comments_num"], self["watch_user_num"], self["click_num"], self['url'],
            self["crawl_time"])

        return insert_sql, sql_params

    def save_to_es(self):
        self.clean_data()
        zhihu = ZhiHuQuestionIndex()
        zhihu.meta.id = self["url_object_id"]
        zhihu.question_id = self["question_id"]
        zhihu.title = self["title"]
        zhihu.content = self["content"]
        zhihu.topics = self["topics"]

        zhihu.answer_num = self["answer_num"]
        zhihu.comments_num = self["comments_num"]
        zhihu.watch_user_num = self["watch_user_num"]
        zhihu.click_num = self["click_num"]
        zhihu.url = self["url"]

        zhihu.crawl_time = self["crawl_time"]

        # 在保存数据时便传入suggest
        zhihu.suggest = generate_suggests(es_zhihu_question,
                                          ((zhihu.title, 10), (zhihu.topics, 7), (zhihu.content, 5)))

        real_time_count('zhihu_question_count', ZHIHU_QUESTION_COUNT_INIT)
        zhihu.save()

    def help_fields(self):
        for field in self.fields:
            print(field, "= scrapy.Field()")


class ZhihuAnswerItem(scrapy.Item, MysqlItem, ElasticSearchItem):
    url_object_id = scrapy.Field()
    answer_id = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()

    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()

    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def clean_data(self):
        try:
            self["praise_num"] = extract_num("".join(self["praise_num"]))
        except BaseException:
            self["praise_num"] = 0
        self["comments_num"] = extract_num("".join(self["comments_num"]))

        self["create_time"] = datetime.datetime.fromtimestamp(
            self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        try:
            self["update_time"] = datetime.datetime.fromtimestamp(
                self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        except:
            self["update_time"] = self["create_time"]

        self["crawl_time"] = self["crawl_time"].strftime(SQL_DATETIME_FORMAT)
        self["content"] = remove_tags(self["content"])

    def save_to_mysql(self):

        self.clean_data()
        # 插入知乎answer表的sql语句
        insert_sql = """
                   insert into zhihu_answer(url_object_id, answer_id, question_id, author_id, author_name,
                   content, praise_num, comments_num,url,create_time,
                   update_time, crawl_time)
                   VALUES (%s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s,
                      %s, %s)
                     ON DUPLICATE KEY UPDATE
                     content=VALUES(content), comments_num=VALUES(comments_num), praise_num=VALUES(praise_num),
                     update_time=VALUES(update_time), author_name=VALUES(author_name)
               """
        sql_params = (
            self["url_object_id"], self["answer_id"], self["question_id"], self["author_id"], self["author_name"],
            self["content"], self["praise_num"], self["comments_num"], self["url"], self["create_time"],
            self["update_time"], self["crawl_time"]
        )

        return insert_sql, sql_params

    def save_to_es(self):
        self.clean_data()
        zhihu = ZhiHuAnswerIndex()

        zhihu.meta.id = self["url_object_id"]
        zhihu.answer_id = self["answer_id"]
        zhihu.question_id = self["question_id"]
        zhihu.author_id = self["author_id"]
        zhihu.author_name = self["author_name"]

        zhihu.content = self["content"]
        zhihu.praise_num = self["praise_num"]
        zhihu.comments_num = self["comments_num"]
        zhihu.url = self["url"]
        zhihu.create_time = self["create_time"]

        zhihu.update_time = self["update_time"]
        zhihu.crawl_time = self["crawl_time"]

        # 在保存数据时便传入suggest
        zhihu.suggest = generate_suggests(es_zhihu_answer,
                                          ((zhihu.author_name, 10), (zhihu.content, 7)))
        real_time_count("zhihu_answer_count", ZHIHU_QUESTION_COUNT_INIT)
        zhihu.save()

    def help_fields(self):
        for field in self.field_list:
            print(field, "= scrapy.Field()")


if __name__ == '__main__':
    instance = ZhihuAnswerItem()
    instance1 = ZhihuQuestionItem()
    print(instance.help_fields())
    print("*" * 30)
    print("self.data_clean()")
    sql, params = fun_sql_insert(field_list=instance.field_list, duplicate_key_update=instance.duplicate_key_update,
                                 table_name=instance.table_name)
    print(sql)
    print(params)

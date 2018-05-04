# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import pickle
import re

from ArticleSpider.settings import SQL_DATETIME_FORMAT
from ArticleSpider.utils.common import extract_num, extract_num_include_dot
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags
from ArticleSpider.models.es_jobbole import ArticleType
from models.es_lagou import LagouType
from models.es_zhihu import ZhiHuQuestionType, ZhiHuAnswerType
from elasticsearch_dsl.connections import connections
# 与es进行连接生成搜索建议
es_article = connections.create_connection(ArticleType._doc_type.using)
es_zhihu_question = connections.create_connection(ZhiHuQuestionType._doc_type.using)
es_lagou = connections.create_connection(LagouType._doc_type.using)
es_zhihu_anwser = connections.create_connection(ZhiHuAnswerType._doc_type.using)
# redis实现抓取数据同步显示
import redis
redis_cli = redis.StrictRedis()
## 设置数据初始值
JOB_COUNT_INIT = 161042
ZHIHU_COUNT_INIT = 173057
JOBBOLE_COUNT_INIT = 5003



class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def gen_suggests(es_con,index, info_tuple):
    es = es_con
    # 根据字符串生成搜索建议数组
    used_words = set()
    # 去重以先来的为主
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyze接口分析字符串：分词并做大小写的转换
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter':["lowercase"]}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words), "weight":weight})

    return suggests


# 字符串转换时间方法
def date_convert(value):
    try:
        value.strip().replace("·", "").strip()
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


# 获取字符串内数字方法
def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


# 去除标签中提取的评论方法
def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


# 直接获取值方法
def return_value(value):
    return value

# 排除none值


def exclude_none(value):
    if value:
        return value
    else:
        value = "无"
        return value

# 自定义itemloader实现默认取第一个值


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class FangItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field(
    )
    price = scrapy.Field()
    address = scrapy.Field()
    tags = scrapy.Field(
    )
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into fang(id, name, price,address, tags, crawl_time
            )
            VALUES (%s, %s, %s,%s, %s, %s) ON DUPLICATE KEY UPDATE  price=VALUES(price)
        """
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        self["crawl_time"] = crawl_time
        self["name"] = self["name"].strip()
        match_hans5 = re.match(
            ".*>([\u4e00-\u9fa5]+)<.*>([\u4e00-\u9fa5]+)<.*>([\u4e00-\u9fa5]+)<.*>([\u4e00-\u9fa5]+)<.*>([\u4e00-\u9fa5]+)<.*",
            self["tags"],
            re.DOTALL)
        match_hans4 = re.match(
            ".*>([\u4e00-\u9fa5]+)<.*>([\u4e00-\u9fa5]+)<.*>([\u4e00-\u9fa5]+)<.*>([\u4e00-\u9fa5]+)<.*",
            self["tags"], re.DOTALL)
        match_hans3 = re.match(
            ".*>([\u4e00-\u9fa5]+)<.*>([\u4e00-\u9fa5]+)<.*>([\u4e00-\u9fa5]+)<.*",
            self["tags"],
            re.DOTALL)
        match_hans2 = re.match(
            ".*>([\u4e00-\u9fa5]+)<.*>([\u4e00-\u9fa5]+)<.*",
            self["tags"],
            re.DOTALL)
        match_hans1 = re.match(
            ".*>([\u4e00-\u9fa5]+)<.*",
            self["tags"],
            re.DOTALL)

        if match_hans5:
            self["tags"] = match_hans5.group(1) + "," + match_hans5.group(2) + match_hans5.group(
                3) + "," + match_hans5.group(4) + "," + match_hans5.group(5)
        elif match_hans4:
            self["tags"] = match_hans4.group(1) + "," + match_hans4.group(
                2) + match_hans4.group(3) + "," + match_hans4.group(4)
        elif match_hans3:
            self["tags"] = match_hans3.group(
                1) + "," + match_hans3.group(2) + "," + match_hans3.group(3)
        elif match_hans2:
            self["tags"] = match_hans2.group(
                1) + "," + match_hans2.group(2)
        elif match_hans1:
            self["tags"] = match_hans1.group(1)
        else:
            self["tags"] = ""
        params = (
            self["id"],
            self["name"],
            self["price"],
            self["address"],
            self["tags"],
            self["crawl_time"])
        return insert_sql, params

# 伯乐在线items类
class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        # input_processor=MapCompose(date_convert),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        # 使用自定义的outprocessor覆盖原始的take first 使得image_url是一个列表。
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        # input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        # list使用逗号连接
        output_processor=Join(",")
    )
    content = scrapy.Field()
    crawl_time = scrapy.Field()

    def make_data_clean(self):
        front_image_url = ""
        # content = remove_tags(self["content"])
        self["crawl_time"] = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        if self["front_image_url"]:
            self["front_image_url"] = self["front_image_url"][0]
        str = self["create_date"].strip().replace("·", "").strip()
        self["create_date"] = datetime.datetime.strptime(str, "%Y/%m/%d").date()
        nums = 0
        value = self["praise_nums"]
        match_re = re.match(".*?(\d+).*", value)
        if match_re:
            nums = int(match_re.group(1))
        else:
            nums = 0
        self["praise_nums"] = nums

    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_article(title, url, url_object_id,create_date, fav_nums, front_image_url, front_image_path,
            praise_nums, comment_nums, tags, content,crawl_time)
            VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s) ON DUPLICATE KEY UPDATE fav_nums=VALUES(fav_nums),praise_nums=VALUES(praise_nums),comment_nums=VALUES(comment_nums),crawl_time=VALUES(crawl_time)
        """
        self.make_data_clean()
        params = (
            self["title"],
            self["url"],
            self["url_object_id"],
            self["create_date"],
            self["fav_nums"],
            self["front_image_url"],
            self["front_image_path"],
            self["praise_nums"],
            self["comment_nums"],
            self["tags"],
            self["content"],
            self["crawl_time"]
        )
        return insert_sql, params

    # 保存伯乐在线文章到es中
    def save_to_es(self):
        self.make_data_clean()
        article = ArticleType()
        article.title = self['title']
        article.create_date = self["create_date"]
        article.content = remove_tags(self["content"])
        article.front_image_url = self["front_image_url"]
        if "front_image_path" in self:
            article.front_image_path = self["front_image_path"]
        article.praise_nums = self["praise_nums"]
        article.fav_nums = self["fav_nums"]
        article.comment_nums = self["comment_nums"]
        article.url = self["url"]
        article.tags = self["tags"]
        article.meta.id = self["url_object_id"]

        # 在保存数据时便传入suggest
        article.suggest = gen_suggests(es_article,ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7),(article.content, 3)))
        if redis_cli.get("jobbole_count"):
            jobbole_count = pickle.loads(redis_cli.get("jobbole_count"))
            jobbole_count = jobbole_count + 1
            jobbole_count = pickle.dumps(jobbole_count)
            redis_cli.set("jobbole_count", jobbole_count)
        else:
            jobbole_count = pickle.dumps(JOBBOLE_COUNT_INIT)
            redis_cli.set("jobbole_count",jobbole_count)
        article.save()


class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field(
        input_processor=MapCompose(exclude_none),
    )
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def make_data_clean(self):
        self["zhihu_id"] = self["zhihu_id"][0]
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

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num,
              watch_user_num, click_num, crawl_time
              )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
              watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """
        self.make_data_clean()
        params = (
            self["zhihu_id"],
            self["topics"],
            self["url"],
            self["title"],
            self["content"],
            self["answer_num"],
            self["comments_num"],
            self["watch_user_num"],
            self["click_num"],
            self["crawl_time"])

        return insert_sql, params
    def save_to_es(self):
        self.make_data_clean()
        zhihu = ZhiHuQuestionType()
        zhihu.zhihu_id = self["zhihu_id"]
        zhihu.topics = self["topics"]
        zhihu.url = self["url"]
        zhihu.title = self["title"]
        zhihu.content = self["content"]
        zhihu.answer_num = self["answer_num"]
        zhihu.comments_num = self["comments_num"]
        zhihu.watch_user_num = self["watch_user_num"]
        zhihu.click_num = self["click_num"]
        zhihu.crawl_time = self["crawl_time"]

         # 在保存数据时便传入suggest
        zhihu.suggest = gen_suggests(es_zhihu_question,ZhiHuQuestionType._doc_type.index, ((zhihu.title, 10), (zhihu.topics, 7),(zhihu.content, 3)))
        if redis_cli.get("zhihu_count"):
            zhihu_count = pickle.loads(redis_cli.get("zhihu_count"))
            zhihu_count = zhihu_count + 1
            zhihu_count = pickle.dumps(zhihu_count)
            redis_cli.set("zhihu_count",zhihu_count)
        else:
            zhihu_count = pickle.dumps(ZHIHU_COUNT_INIT)
            redis_cli.set("zhihu_count",zhihu_count)
        zhihu.save()

class ZhihuAnswerItem(scrapy.Item):
    # 知乎的问题回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()
    author_name = scrapy.Field()

    def make_data_clean(self):
        self["create_time"] = datetime.datetime.fromtimestamp(
            self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        self["update_time"] = datetime.datetime.fromtimestamp(
            self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        self["crawl_time"] = self["crawl_time"].strftime(SQL_DATETIME_FORMAT)
        self["content"] = remove_tags(self["content"])

    def get_insert_sql(self):
        # 插入知乎answer表的sql语句
        insert_sql = """
            insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, praise_num, comments_num,
              create_time, update_time, crawl_time,author_name
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
              ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), praise_num=VALUES(praise_num),
              update_time=VALUES(update_time), author_name=VALUES(author_name)
        """
        self.make_data_clean()
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["praise_num"],
            self["comments_num"], self["create_time"], self["update_time"],
            self["crawl_time"],
            self["author_name"],
        )

        return insert_sql, params
    def save_to_es(self):
        self.make_data_clean()
        zhihu = ZhiHuAnswerType()
        zhihu.zhihu_id = self["zhihu_id"]
        zhihu.url = self["url"]
        zhihu.question_id = self["question_id"]
        zhihu.author_id = self["author_id"]
        zhihu.content = self["content"]
        zhihu.praise_num = self["praise_num"]
        zhihu.comments_num = self["comments_num"]
        zhihu.create_time = self["create_time"]
        zhihu.update_time = self["update_time"]
        zhihu.crawl_time = self["crawl_time"]
        zhihu.author_name = self["author_name"]

        # 在保存数据时便传入suggest
        zhihu.suggest = gen_suggests(es_zhihu_anwser,ZhiHuAnswerType._doc_type.index,
                                     ((zhihu.author_name, 10), (zhihu.content, 7)))
        if redis_cli.get("zhihu_count"):
            zhihu_count = pickle.loads(redis_cli.get("zhihu_count"))
            zhihu_count = zhihu_count + 1
            zhihu_count = pickle.dumps(zhihu_count)
            redis_cli.set("zhihu_count",zhihu_count)
        else:
            zhihu_count = pickle.dumps(ZHIHU_COUNT_INIT)
            redis_cli.set("zhihu_count",zhihu_count)
        zhihu.save()

def remove_splash(value):
    # 去掉工作城市的斜线
    return value.replace("/", "")


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    # 拉勾网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years_min = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years_max = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(",")
    )
    crawl_time = scrapy.Field()

    def make_data_clean(self):
        match_obj1 = re.match("经验(\d+)-(\d+)年", self['work_years_min'])
        match_obj2 = re.match("经验应届毕业生", self['work_years_min'])
        match_obj3 = re.match("经验不限", self['work_years_min'])
        match_obj4 = re.match("经验(\d+)年以下", self['work_years_min'])
        match_obj5 = re.match("经验(\d+)年以上", self['work_years_min'])

        if match_obj1:
            self['work_years_min'] = match_obj1.group(1)
            self['work_years_max'] = match_obj1.group(2)
        elif match_obj2:
            self['work_years_min'] = 0.5
            self['work_years_max'] = 0.5
        elif match_obj3:
            self['work_years_min'] = 0
            self['work_years_max'] = 0
        elif match_obj4:
            self['work_years_min'] = 0
            self['work_years_max'] = match_obj4.group(1)
        elif match_obj5:
            self['work_years_min'] = match_obj4.group(1)
            self['work_years_max'] = match_obj4.group(1)+100
        else:
            self['work_years_min'] = 999
            self['work_years_max'] = 999

        match_salary = re.match("(\d+)[Kk]-(\d+)[Kk]", self['salary_min'])
        if match_salary:
            self['salary_min'] = match_salary.group(1)
            self['salary_max'] = match_salary.group(2)
        else:
            self['salary_min'] = 666
            self['salary_max'] = 666
        match_time1 = re.match("(\d+):(\d+).*", self["publish_time"])
        match_time2 = re.match("(\d+)天前.*", self["publish_time"])
        match_time3 = re.match("(\d+)-(\d+)-(\d+)", self["publish_time"])
        if match_time1:
            today = datetime.datetime.now()
            hour = int(match_time1.group(1))
            minutues = int(match_time1.group(2))
            time = datetime.datetime(
                today.year, today.month, today.day, hour, minutues)
            self["publish_time"] = time.strftime(SQL_DATETIME_FORMAT)
        elif match_time2:
            days_ago = int(match_time2.group(1))
            today = datetime.datetime.now() - datetime.timedelta(days=days_ago)
            self["publish_time"] = today.strftime(SQL_DATETIME_FORMAT)
        elif match_time3:
            year = int(match_time3.group(1))
            month = int(match_time3.group(2))
            day = int(match_time3.group(3))
            today = datetime.datetime(year, month, day)
            self["publish_time"] = today.strftime(SQL_DATETIME_FORMAT)
        else:
            self["publish_time"] = datetime.datetime.now(
            ).strftime(SQL_DATETIME_FORMAT)
        self["crawl_time"] = self["crawl_time"].strftime(SQL_DATETIME_FORMAT)

    def get_insert_sql(self):
        insert_sql = """
            insert into lagou_job(title, url, url_object_id, salary_min, salary_max, job_city, work_years_min, work_years_max, degree_need,
            job_type, publish_time, job_advantage, job_desc, job_addr, company_name, company_url,
            tags, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE salary_min=VALUES(salary_min), salary_max=VALUES(salary_max), job_desc=VALUES(job_desc)
        """
        self.make_data_clean()
        params = (
            self["title"],
            self["url"],
            self["url_object_id"],
            self["salary_min"],
            self["salary_max"],
            self["job_city"],
            self["work_years_min"],
            self["work_years_max"],
            self["degree_need"],
            self["job_type"],
            self["publish_time"],
            self["job_advantage"],
            self["job_desc"],
            self["job_addr"],
            self["company_name"],
            self["company_url"],
            self["tags"],
            self["crawl_time"]
        )

        return insert_sql, params

     # 保存拉勾网职位到es中
    def save_to_es(self):
        self.make_data_clean()
        job = LagouType()
        job.title = self["title"]
        job.url = self["url"]
        job.url_object_id = self["url_object_id"]
        job.salary_min = self["salary_min"]
        job.salary_max = self["salary_max"]
        job.job_city = self["job_city"]
        job.work_years_min = self["work_years_min"]
        job.work_years_max = self["work_years_max"]
        job.degree_need = self["degree_need"]
        job.job_desc = remove_tags(self["job_desc"]).strip().replace("\r\n", "").replace("\t", "")
        job.job_advantage = self["job_advantage"]
        job.tags = self["tags"]
        job.job_type = self["job_type"]
        job.publish_time = self["publish_time"]
        job.job_addr = self["job_addr"]
        job.company_name = self["company_name"]
        job.company_url = self["company_url"]
        job.crawl_time = self['crawl_time']

        # 在保存数据时便传入suggest
        job.suggest = gen_suggests(es_lagou, LagouType._doc_type.index,
                                     ((job.title, 10), (job.tags, 7), (job.job_advantage, 6),(job.job_desc,5),(job.job_addr, 4),(job.company_name,8),(job.degree_need,3),(job.job_city,9)))
        if redis_cli.get("job_count"):
            job_count = pickle.loads(redis_cli.get("job_count"))
            job_count = job_count + 1
            job_count = pickle.dumps(job_count)
            redis_cli.set("job_count",job_count)
        else:
            job_count = pickle.dumps(JOB_COUNT_INIT)
            redis_cli.set("job_count",job_count)
        job.save()


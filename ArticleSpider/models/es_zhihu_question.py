# _*_ coding: utf-8 _*_
__author__ = 'mtianyan'
__date__ = '2017/6/25 15:45'


from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

class ZhiHuType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    #伯乐在线文章类型
    # 知乎的问题 item
    zhihu_id = Keyword()
    topics = Keyword()
    url = Keyword()
    title = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")
    answer_num = Integer()
    comments_num =Integer()
    watch_user_num = Integer()
    click_num = Integer()
    crawl_time =Date()

    class Meta:
        index = "zhihu"
        doc_type = "question"


if __name__ == "__main__":
    ZhiHuType.init()

# _*_ coding: utf-8 _*_
__author__ = 'mtianyan'
__date__ = '2017/6/25 10:18'


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

class LagouType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    url =  Keyword()
    url_object_id = Keyword()
    salary = Text(analyzer="ik_max_word")
    job_city = Keyword()
    work_years = Text(analyzer="ik_max_word")
    degree_need = Text(analyzer="ik_max_word")
    job_type = Keyword()
    publish_time = Text(analyzer="ik_max_word")
    job_advantage = Text(analyzer="ik_max_word")
    job_desc = Text(analyzer="ik_max_word")
    job_addr = Text(analyzer="ik_max_word")
    company_name = Keyword()
    company_url = Keyword()
    tags = Text(analyzer="ik_max_word")
    crawl_time = Date()

    class Meta:
        index = "lagou"
        doc_type = "job"


if __name__ == "__main__":
    LagouType.init()

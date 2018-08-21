from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

__author__ = 'mtianyan'
__date__ = '2017/6/24 22:57'

connections.create_connection(hosts=["localhost"])

my_analyzer = analyzer('ik_smart')


class JobboleBlogIndex(Document):
    """伯乐在线文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    url_object_id = Keyword()
    front_image_url = Keyword()
    praise_nums = Integer()
    comment_nums = Integer()
    fav_nums = Integer()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_smart")

    class Index:
        name = 'jobbole_blog'


if __name__ == "__main__":
    JobboleBlogIndex.init()

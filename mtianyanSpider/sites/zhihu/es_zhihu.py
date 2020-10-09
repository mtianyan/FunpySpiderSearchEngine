from elasticsearch_dsl import connections, Document, Keyword, Text, Integer, Date, Completion, analyzer

from config import ES_HOST

connections.create_connection(hosts=[ES_HOST])

my_analyzer = analyzer('ik_smart')


class ZhiHuQuestionIndex(Document):
    question_id = Keyword()
    topics = Text(analyzer="ik_max_word")
    url = Keyword()
    title = Text(analyzer="ik_max_word")
    title_keyword = Keyword()
    content = Text(analyzer="ik_max_word")
    answer_num = Integer()
    comments_num = Integer()
    watch_user_num = Integer()
    click_num = Integer()

    crawl_time = Date()

    class Index:
        name = 'zhihu_question'


class ZhiHuAnswerIndex(Document):
    answer_id = Keyword()
    question_id = Keyword()
    author_id = Keyword()
    author_name = Keyword()

    content = Text(analyzer="ik_smart")
    praise_num = Keyword()
    comments_num = Integer()
    url = Keyword()
    create_time = Date()

    update_time = Date()
    crawl_time = Date()

    class Index:
        name = 'zhihu_answer'


if __name__ == "__main__":
    ZhiHuQuestionIndex.init()
    ZhiHuAnswerIndex.init()

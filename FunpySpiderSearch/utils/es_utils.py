__author__ = 'mtianyan'
__date__ = '2018/8/20 07:53'


def generate_suggests(es_con, info_tuple):
    es = es_con
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            words = es.indices.analyze(index="jobbole_blog",
                                       body={"analyzer": "ik_max_word", "text": "{0}".format(text)})
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests

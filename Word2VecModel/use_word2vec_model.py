from gensim.models import KeyedVectors
import gensim


def test_us_small_model():
    model = gensim.models.Word2Vec.load("./trained_models/zhihu.model")
    print(model.wv.most_similar('老公', topn=8))
    print("*" * 20)


def test_tencent_ai_model():
    model = KeyedVectors.load_word2vec_format("./trained_models/45000-small.txt")
    print(model.most_similar('特朗普', topn=10))
    print("*" * 20)
    print(model.most_similar(positive=['女', '国王'], negative=['男'], topn=1))
    print("*" * 20)
    print(model.doesnt_match("上海 成都 广州 北京".split(" ")))
    print("*" * 20)
    print(model.similarity('女人', '男人'))


def test_zhihu_model():
    model = KeyedVectors.load_word2vec_format("./trained_models/sgns.zhihu.bigram-char")
    print(model.most_similar('特朗普', topn=10))
    print("*" * 20)
    print(model.most_similar(positive=['女', '国王'], negative=['男'], topn=1))
    print("*" * 20)
    print(model.doesnt_match("上海 成都 广州 北京".split(" ")))
    print("*" * 20)
    print(model.similarity('女人', '男人'))


if __name__ == '__main__':
    print("使用我们自己训练的微型知乎wordvec模型: ")
    test_us_small_model()
    print("使用腾讯ai实验室word2vec模型: ")  # https://ai.tencent.com/ailab/nlp/embedding.html
    test_tencent_ai_model()
    print("使用中文开源知乎word2vec模型")     # https://github.com/Embedding/Chinese-Word-Vectors
    test_zhihu_model()

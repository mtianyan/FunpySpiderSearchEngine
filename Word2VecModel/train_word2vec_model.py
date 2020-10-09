def model_train(train_file_name, save_model_name):  # model_file_name为训练语料的路径,save_model为保存模型名
    from gensim.models import word2vec
    import gensim
    sentences = word2vec.Text8Corpus(train_file_name)   # 加载语料
    model = gensim.models.Word2Vec(sentences, size=200)  # 训练skip-gram模型; 默认window=5
    model.save(save_model_name)
    # model.wv.save_word2vec_format(save_model_name + ".model", binary=True)


if __name__ == '__main__':
    model_train("./cleaned_data/zhihu.txt_cuted.txt", "./trained_models/zhihu.model")

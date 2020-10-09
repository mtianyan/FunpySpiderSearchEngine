1. trans_raw_data_to_clean.py

> 转换原始爬虫存储数据到clean data

2. cut_the_cleaned_data.py

> 此函数作用是对经知乎question和answer.csv 合并的txt文件 进行分词处理后，作为训练模型的语料

3. train_word2vec_model.py

> 训练word2vec模型

4. use_word2vec_model.py

>模型使用的示例。

```
    print("使用腾讯ai实验室word2vec模型: ")  # https://ai.tencent.com/ailab/nlp/embedding.html
    test_tencent_ai_model()
    print("使用中文开源知乎word2vec模型")     # https://github.com/Embedding/Chinese-Word-Vectors
```


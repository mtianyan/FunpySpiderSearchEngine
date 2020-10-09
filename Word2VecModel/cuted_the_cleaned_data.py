def jieba_cut_word(raw_file):
    """此函数作用是对经知乎question和answer.csv 合并的txt文件 进行分词处理后，作为训练模型的语料"""
    import jieba
    global cuted_file     # 分词之后保存的文件名
    cuted_file = raw_file + '_cuted.txt'

    with open(raw_file, 'r', encoding='utf-8') as f_raw:
        text = f_raw.read()  # 获取文本内容
        cuted_text = jieba.cut(text, cut_all=False)  # 精确模式
        str_out = ' '.join(cuted_text).replace('，', '').replace('。', '').replace('？', '').replace('！', '') \
            .replace('“', '').replace('”', '').replace('：', '').replace('…', '').replace('（', '').replace('）', '') \
            .replace('—', '').replace('《', '').replace('》', '').replace('、', '').replace('‘', '') \
            .replace('’', '')     # 去掉标点符号
    with open(cuted_file, 'w', encoding='utf-8') as f_cuted:
        f_cuted.write(str_out)


if __name__ == '__main__':
    jieba_cut_word("./cleaned_data/zhihu.txt")

import pandas as pd

zhihu_question = pd.read_csv('./raw_data/zhihu_question.csv', encoding="gb2312")
zhihu_answer = pd.read_csv('./raw_data/zhihu_answer.csv', encoding="gb2312")
with open("./cleaned_data/zhihu.txt", 'w') as f_cleaned:
    for title in zhihu_question["title"]:
        f_cleaned.write(title)
        f_cleaned.write("\n")
    for content in zhihu_answer["content"]:
        f_cleaned.write(content)
        f_cleaned.write("\n")

# coding:utf-8
# @Time : 2021/11/28 15:57
# @Author : 郑攀
# @File ： calculate.py
# @Software : PyCharm
import csv

import os
path = 'new data/'
files = os.listdir(path)

print(files)

fp = open('各景点数据.csv', "w+", encoding='utf8', newline='')
write = csv.writer(fp)

for p in range(len(files)):

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    dictionary = ['环境和景观','文化和历史价值','设施和服务','性价比']

    doc_set = []
    with open(path + files[p], "r", encoding='utf-8') as f:  # 打开文件
        read = csv.reader(f)
        for line in read:
            doc_set.append(line)

    print(files[p])
    for i in range(0,len(dictionary)):
        sentiment = []
        for j in range(0,len(doc_set)):
            if dictionary[i]==doc_set[j][0]:
                sentiment.append(doc_set[j][7])
        sentiment_2 = sentiment.count('2')
        positive = sentiment_2/len(sentiment)
        print([files[p],dictionary[i],positive])
        write.writerow([files[p].replace('.csv',''),dictionary[i],positive])
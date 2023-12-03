# coding:utf-8
# @Time : 2021/11/19 14:46
# @Author : 郑攀
# @File ： conversion.py
# @Software : PyCharm
import csv
import os
import time
import json, requests
import sys

import chardet
import numpy as np
import synonyms
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# -*- coding: utf-8 -*-
# 加载自定义词
import jieba
import re
import warnings
warnings.filterwarnings("ignore")
from aip import AipNlp
APP_ID = '42753563'
API_KEY = 'SVK726P3CReEDkfFZgKcjfR5'
SECRET_KEY = 'DuUObAeoeXyVBU8kEnhrTDnLPofYyCoU'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

# result = synonyms.compare('文化底蕴', '文化和历史价值', seg=False)
# print(result)

stop_table = ['你', '了', '我', '啊', '是', '呢', '吧', '的', '地', '呀', '个', '哪', '在', '非常', '和', '好', '很', '又', '有', '还',
              '上', '都', '也', '起来', '不', '?', '选', '用', '大', '高', '就', '给',
              '着', '快', '买', '这',  '吗', '什么', '怎么', 'hellip',
              '!', '.', '？', '！', '。', '…', '，', ',', '、', '/', '+', '_', '-', '*', '-', '&', '@', '(', ')', '%', '$',
              '#', ' ', ':', '：', ';', '[', ']', "'", '\\', 'n', '~', '（', '）','	','','\n']
dictionary = ['环境和景观','文化和历史价值','设施和服务','性价比']
def format1(list1):
    a = []
    for s in list1:
        a1 = list(jieba.cut(s))
        a.append(a1)
    for i in range(0, len(a)):
        # print(a[i])
        for item in stop_table:
            while item in a[i]:
                a[i].remove(item)

    return a

import os
path = 'raw data/'
files = os.listdir(path)

for p in range(len(files)):
    doc_set = []
    print(files[p])
    with open(path + files[p], "r", encoding='utf8') as f:  # 打开文件
        read = csv.reader(f)
        next(read)
        for line in read:
            doc_set.append(line[2])
    sentences = format1(doc_set)

    pattern = r'“,|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'

    fp = open('new data/' + files[p], 'w+', newline='', encoding='utf-8')
    write = csv.writer(fp)
    write.writerow(['字典属性','商品属性','相似性','商品属性所在短句','短句积极性','短句消极性','置信度','情感类别'])
    for i in range(0, len(sentences)):
        try:
            result_list = re.split(pattern, doc_set[i])
            for word in sentences[i]:
                for dic in dictionary:
                    if word and dic:
                        result = synonyms.compare(word, dic, seg=False)
                        if result > 0.55:
                            for short_sentence in result_list:
                                if word in short_sentence:
                                    sentiment = client.sentimentClassify(short_sentence)
                                    print(p, i, word, dic, sentiment)
                                    positive = str(sentiment['items'][0]['positive_prob'])
                                    negative = str(sentiment['items'][0]['negative_prob'])
                                    confidence = str(sentiment['items'][0]['confidence'])
                                    emotion = str(sentiment['items'][0]['sentiment'])
                                    string = [dic, word, result, short_sentence, positive, negative, confidence, emotion]
                                    write.writerow(string)
                                    time.sleep(1)

        except:
            print(sentences[i])
    fp.close()
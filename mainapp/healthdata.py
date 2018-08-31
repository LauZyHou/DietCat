# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 13:35:00 2018

@author: 45431
"""
import numpy as np
from sklearn.cross_validation import cross_val_score, ShuffleSplit
from sklearn.ensemble import RandomForestRegressor
import pymongo
from pymongo import MongoClient
import pandas as pd

client = MongoClient('localhost', 27017)
db = client['dietcat']
posts = db.XJUdata
names = ['BMI', '肺活量', '立定跳远', '坐位体前屈', '仰卧起坐/引体向上', '50米跑', '长跑时间']


def getbasedata(sex='男'):
    X_data = []
    X_target = []
    datas = posts.find({'性别': sex})
    for item in datas:
        X_data.append(item['数据'])
        X_target.append(item['总分'])
    return X_data, X_target


def AllDataDeal(X_data, X_target):
    X_data=np.array(X_data)
    X_target=np.array(X_target)
    names = ['BMI', '肺活量', '立定跳远', '坐位体前屈', '仰卧起坐/引体向上', '50米跑', '长跑时间']
    rf = RandomForestRegressor(max_features='sqrt')
    scores = []
    score_value = []
    score_name = []
    # 单独采用每个特征进行建模，并进行交叉验证
    # print(len(X_data))
    for i in range(len(names)):
        score = cross_val_score(rf, X_data[:, i:i + 1], X_target, scoring="r2", cv=ShuffleSplit(len(X_data), 3, .3))
        scores.append((format(np.abs(np.mean(score)), '.3f'), names[i]))
        # scores.append((format(np.mean(score), '.3f'), names[i]))
        score_value.append(abs(np.mean(score)))
        score_name.append(names[i])
    return sorted(scores, reverse=True)

#    print(score_value)
#    print(score_name)
#    plt.bar(range(len(score_value)), score_value,fc='r',tick_label=score_name)
def HealthWeight(sex):
    X_data, X_target=getbasedata(sex)
    return AllDataDeal(X_data, X_target)

def avgstandard(grade='all',sex='1'):
    if sex =='1' or sex is None:
        sex='男'
    else:
        sex='女'
    Datas=[]
    if grade=='all':
        data = posts.find({'性别':sex})
        for item in data:
            Datas.append([item['数据'][4],item['数据'][1],item['数据'][0],item['数据'][2],])
        df = pd.DataFrame(Datas, columns=['仰卧起坐', '肺活量', 'BMI', '立定跳远'])
        a = df.mean()
        print(a)
        return [a[0],5,a[1],a[2],5,a[3]]
    else:
        data = posts.find({'等级':grade,'性别':sex})
        for item in data:
            Datas.append([item['数据'][4],item['数据'][1],item['数据'][0],item['数据'][2],])
        df=pd.DataFrame(Datas,columns=['仰卧起坐', '肺活量','BMI','立定跳远'])
        a=df.mean()
        return [a[0], 5.3, a[1], a[2], 5.3, a[3]]




'''
print(HealthWeight('女'))
print(HealthWeight('男'))
avgstandard()
avgstandard('优秀','1')




girl_data, girl_target = getbasedata('女')
AllDataDeal(girl_data, girl_target)
boy_data,boy_target=getbasedata('男')
AllDataDeal(boy_data,boy_target)
'''

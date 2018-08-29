# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 13:35:00 2018

@author: 45431
"""

import pandas as pd
import numpy as np
from sklearn.cross_validation import cross_val_score, ShuffleSplit
from sklearn.ensemble import RandomForestRegressor

def TimeSum(a):
    return float(int(a) * 60 + (a - int(a)) * 100)


def BMI(a, b):
    return (b / np.square(a / 100))


data = pd.read_csv('XJUStudentData.csv', sep=',')
a = data.loc[data['身高'] > 0]
b = a[['总分', '性别', '总分等级', '身高', '体重', '肺活量', '立定跳远', '坐位体前屈', '仰卧起坐', '引体向上', '50米跑', '800米跑', '1000米跑']]
b['BMI'] = b.apply(lambda x: BMI(x['身高'], x['体重']), axis=1)

boy = b.loc[b['性别'] == '男']
boy['仰卧起坐/引体向上'] = boy['引体向上']
boy = boy[['总分', 'BMI', '肺活量', '立定跳远', '坐位体前屈', '仰卧起坐/引体向上', '50米跑', '800米跑', '1000米跑']]
boy['长跑时间'] = boy['1000米跑'].apply(lambda x: TimeSum(x))
boy = boy[['总分', 'BMI', '肺活量', '立定跳远', '坐位体前屈',
           '仰卧起坐/引体向上', '50米跑', '长跑时间']]
girl = b.loc[b['性别'] == '女']
girl['仰卧起坐/引体向上'] = girl['仰卧起坐']
girl = girl[['总分', 'BMI', '肺活量', '立定跳远', '坐位体前屈', '仰卧起坐/引体向上', '50米跑', '800米跑', '1000米跑']]
girl['长跑时间'] = girl['800米跑'].apply(lambda x: TimeSum(x))
girl = girl[['总分', 'BMI', '肺活量', '立定跳远', '坐位体前屈',
             '仰卧起坐/引体向上', '50米跑', '长跑时间']]
print(boy)
print(np.array(boy)[0][0])


def AllDataDeal(X):
    names = ['BMI', '肺活量', '立定跳远', '坐位体前屈', '仰卧起坐/引体向上', '50米跑', '长跑时间']
    X_data = np.array(X[names])
    #    print(X_data)
    X_target = np.array(X['总分'])
    #    print(X_target)

    rf = RandomForestRegressor(max_features='sqrt')
    scores = []
    score_value = []
    score_name = []
    # 单独采用每个特征进行建模，并进行交叉验证
    print(X_data.shape[1])
    for i in range(X_data.shape[1]):
        score = cross_val_score(rf, X_data[:, i:i + 1], X_target, scoring="r2", cv=ShuffleSplit(len(X_data), 3, .3))
        scores.append((format(abs(np.mean(score)), '.3f'), names[i]))
        score_value.append(abs(np.mean(score)))
        score_name.append(names[i])
    print(sorted(scores, reverse=True))


#    print(score_value)
#    print(score_name)
#    plt.bar(range(len(score_value)), score_value,fc='r',tick_label=score_name)


AllDataDeal(girl)
AllDataDeal(boy)

import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['dietcat']
posts = db.XJUdata



def TimeSum(a):
	return float(int(a)*60+(a-int(a))*100)

def BMI(a,b):
    return (b/np.square(a/100))


data=pd.read_csv('XJUStudentData.csv',sep=',')
a=data.loc[data['身高']>0]
a=a.loc[a['50米跑']>0]


b=a[['姓名','总分','性别','总分等级','身高','体重','肺活量','立定跳远','坐位体前屈', '仰卧起坐', '引体向上', '50米跑', '800米跑', '1000米跑']]
b['BMI'] = b.apply(lambda x: BMI(x['身高'],x['体重']), axis=1)

boy=b.loc[b['性别']=='男']
boy['仰卧起坐/引体向上'] = boy['引体向上']
boy=boy[['姓名','总分','BMI','肺活量','立定跳远','坐位体前屈','仰卧起坐/引体向上', '50米跑', '800米跑', '1000米跑']]
boy['长跑时间'] = boy['1000米跑'].apply(lambda x: TimeSum(x))
boy=boy[['总分','BMI','肺活量','立定跳远','坐位体前屈',
         '仰卧起坐/引体向上', '50米跑', '长跑时间','姓名']]
girl=b.loc[b['性别']=='女']
girl['仰卧起坐/引体向上'] = girl['仰卧起坐']
girl=girl[['姓名','总分','BMI','肺活量','立定跳远','坐位体前屈', '仰卧起坐/引体向上', '50米跑', '800米跑', '1000米跑']]
girl['长跑时间'] = girl['800米跑'].apply(lambda x: TimeSum(x))
girl=girl[['总分','BMI','肺活量','立定跳远','坐位体前屈',
           '仰卧起坐/引体向上', '50米跑', '长跑时间','姓名']]
for girls in np.array(girl):
    post_data = {
        '总分': girls[0],
        'BMI': girls[1],
        '肺活量': girls[2],
        '立定跳远': girls[3],
        '坐位体前屈': girls[4],
        '仰卧起坐/引体向上': girls[5],
        '50米跑': girls[6],
        '长跑时间': girls[7],
        '姓名':girls[8],
        '性别':'女'
    }
    result = posts.insert_one(post_data)
    print('One post: {0}'.format(result.inserted_id))

for girls in np.array(boy):
    post_data = {
        '总分': girls[0],
        'BMI': girls[1],
        '肺活量': girls[2],
        '立定跳远': girls[3],
        '坐位体前屈': girls[4],
        '仰卧起坐/引体向上': girls[5],
        '50米跑': girls[6],
        '长跑时间': girls[7],
        '姓名':girls[8],
        '性别':'男'
    }
    result = posts.insert_one(post_data)
    print('One post: {0}'.format(result.inserted_id))

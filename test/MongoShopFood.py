import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np

client = MongoClient('localhost', 27017)
db = client['dietcat']
posts = db.ShopFood


def change(i):
    if '起' in i:
        print(i[:-1])
        return float(i[:-1])
    else:
        print(i)
        return float(i)


data = pd.read_csv('ShopFood2.csv', sep=',')
a = data.loc[data['推荐人数'] > 0]
a['价格'] = a.apply(lambda x: change(x['价格']), axis=1)
a = a.loc[a['价格'] > 5]
print(len(a))
for item in np.array(a):
    print(item[4][0:2])
    if item[4][0:2] in ['07', '08', '09']:
        post_data = {
            '商铺名称': item[0],
            '商铺图标网址': item[1],
            '商铺链接': item[2],
            '商铺评分': item[3],
            '商铺营业时间': item[4],
            '菜品': item[5],
            '菜品图标网址': item[6],
            '推荐人数': item[7],
            '价格': item[8],
            '早市': True
        }
    else:
        post_data = {
            '商铺名称': item[0],
            '商铺图标网址': item[1],
            '商铺链接': item[2],
            '商铺评分': item[3],
            '商铺营业时间': item[4],
            '菜品': item[5],
            '菜品图标网址': item[6],
            '推荐人数': item[7],
            '价格': item[8],
            '早市': False
        }

    result = posts.insert_one(post_data)
    # print('One post: {0}'.format(result.inserted_id))

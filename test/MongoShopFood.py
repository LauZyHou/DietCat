import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['dietcat']
posts = db.ShopFood

data = pd.read_csv('ShopFood.csv', sep=',')
print(data)
a = data.loc[data['推荐人数'] > 0]
for item in np.array(data):
    post_data = {
        '商铺名称': item[0],
        '商铺图标网址': item[1],
        '商铺链接': item[2],
        '商铺评分': item[3],
        '商铺营业时间': item[4],
        '菜品': item[5],
        '菜品图标网址': item[6],
        '推荐人数': item[7],

    }
    result = posts.insert_one(post_data)
    print('One post: {0}'.format(result.inserted_id))

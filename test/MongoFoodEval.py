import pymongo
from pymongo import MongoClient
import random

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['dietcat']
posts = db.FoodEval
name=['lzh','ghj','zhy','Durant','dll']
f=db.ShopFood.find({},{'推荐人数':1, '菜品':1,'商铺名称':1,"_id": 0})
foods=[]
shops=[]
for i in f:
    if i['推荐人数']>10:
        foods.append(i['菜品'])
        shops.append(i['商铺名称'])

print(len(foods))

for people in name:
    for i in range(len(foods)):
        post_data = {
        '用户': people,
        '菜品': shops[i]+'-'+foods[i],
        '评分': random.randint(0,5),
    }
        result = posts.insert_one(post_data)
        print('One post: {0}'.format(result.inserted_id))

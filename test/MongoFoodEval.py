import pymongo
from pymongo import MongoClient
import random

client = MongoClient('localhost', 27017)
db = client['dietcat']
posts = db.FoodEval
UserData = db.UserData
name = []
e = db.user.find({}, {'password': 1, 'username': 1})
for i in e:
    print(i.get('_id').__str__())
    name.append(i.get('_id').__str__())
f = db.ShopFood.find({}, {'推荐人数': 1, '菜品': 1, '商铺名称': 1, "_id": 0})
foods = []
shops = []
for i in f:
    if i['推荐人数'] > 15:
        foods.append(i['菜品'])
        shops.append(i['商铺名称'])

print(len(foods))

for people in name:
    for i in range(len(foods)):
        post_data = {
            '用户': people,
            '菜品': shops[i] + '-' + foods[i],
            '评分': random.randint(0, 5),
        }
        result = posts.insert_one(post_data)
        print('One post: {0}'.format(result.inserted_id))
    post_data = {
        '用户': people,
        '时间': None,
        '睡眠时长': None,
        '运动时长': None,
        '步行距离': None,
        '工作': None,
        '食物': None,
    }
    esult = UserData.insert_one(post_data)
    print('One post: {0}'.format(result.inserted_id))

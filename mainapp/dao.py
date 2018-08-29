from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import random
import re

# 连接到MongoDB
conn = MongoClient('127.0.0.1', 27017)
# 获取dietcat这个DB对象
db_dietcat = conn.dietcat


# 检查某个dict的条件在user集合中满足的文档数目,可用于注册前的检查
def docCountInUser(dict):
    # print(db_dietcat.user.find(dict).count())
    return db_dietcat.user.find(dict).count()


# 向user集合中添加一个用户,可用于注册
def addDocInUser(dict):
    db_dietcat.user.insert(dict)


# 按字典查询第一个user记录
def firstDocInUser(dict):
    return db_dietcat.user.find_one(dict)  # 可能是None


# 修改一个满足条件的user
def updateOneUser(dict_where, dict_set):
    db_dietcat.user.update(dict_where, dict_set)  # update方法只更新一个


def username2ID(name):
    return db_dietcat.user.find_one({'username':name}).get('_id').__str__()  # 可能是None


def RecommendList(list):
    RMDLIST = []
    for i in list:
        RMDfood = db_dietcat.ShopFood.find_one({'商铺名称': i.split("-")[0], '菜品': i.split("-")[1]})
        RMDfood['id'] = RMDfood.get('_id').__str__()
        RMDLIST.append(RMDfood)
    return RMDLIST


def ID2Pic(id):
    return db_dietcat.ShopFood.find_one({'_id': ObjectId(id)})['商铺链接']


def ID2ShopName(id):
    return db_dietcat.ShopFood.find_one({'_id': ObjectId(id)})['商铺名称'] + "-" + \
           db_dietcat.ShopFood.find_one({'_id': ObjectId(id)})['菜品']


def OneDayRecommend(list):
    RMDLIST = []
    Flag_breakfast = 0
    for i in list:
        RMDfood = db_dietcat.ShopFood.find_one({'商铺名称': i.split("-")[0], '菜品': i.split("-")[1]})
        RMDfood['id'] = RMDfood.get('_id').__str__()
        if RMDfood.get('早市'):
            if Flag_breakfast == 0:
                breakfast = RMDfood
                sneak = RMDfood
            else:
                sneak = RMDfood
        else:
            RMDLIST.append(RMDfood)
    return breakfast, RMDLIST[0:2], sneak


def favouriateFood(username):
    favourityfood = []
    UserEval = db_dietcat.FoodEval.find({'用户': username})
    for usereval in UserEval:
        if usereval['评分'] > 3:
            favourityfood.append(usereval)
    foodrandom = random.sample(favourityfood, 12)
    Food = []
    for item in foodrandom:
        food = db_dietcat.ShopFood.find_one({'商铺名称': item['菜品'].split("-")[0], '菜品': item['菜品'].split("-")[1]})
        food['id'] = food.get('_id').__str__()
        Food.append(food)
    return Food


def hotFood():
    hotfood = []
    scotts_posts = db_dietcat.ShopFood.find({}, {"_id": 0})
    for i in scotts_posts:
        if i['推荐人数'] > 50:
            i['id'] = i.get('_id').__str__()
            hotfood.append(i)
    return random.sample(hotfood, 12)


def FoodNotEnough(num=70):
    food = db_dietcat.FoodEval.aggregate([{"$sample": {"size": num}}])
    return [item['菜品'] for item in food]


def updateuserdata(dict_where, dict_set):
    db_dietcat.UserData.update(dict_where, dict_set)


def IFdateinData(dict):
    return db_dietcat.UserData.find_one(dict)


def inputuserdata(useid, date, sleeptime=None, sporttime=None, walk=None, joblist=None, foodlist=None):
    result = db_dietcat.UserData.insert_one({
        '用户': useid,
        '时间': date,
        '睡眠时长': sleeptime,
        '运动时长': sporttime,
        '步行距离': walk,
        '工作': joblist,
        '食物': foodlist,
    })
    print('One post: {0}'.format(result.inserted_id))

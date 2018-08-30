from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import random
import re
import datetime

start = '2017-12-31'
end = '2018-12-31'

datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
monthday = []
while datestart < dateend:
    datestart += datetime.timedelta(days=1)
    monthday.append(datestart.strftime('%m-%d'))

# 连接到MongoDB
conn = MongoClient('127.0.0.1', 27017)
# 获取dietcat这个DB对象
db_dietcat = conn.dietcat

day = []
for i in range(3):
    for j in range(10):
        day.append(str(i) + str(j))
day = day[1:30]
day.extend(['30', '31'])


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


# 删除满足条件的用户
def deleteTheUser(dic):
    db_dietcat.user.remove(dic)  # 只删除第一个用户；
def username2ID(name):
    return db_dietcat.user.find_one({'username': name}).get('_id').__str__()  # 可能是None


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
    if len(favourityfood) > 12:
        foodrandom = random.sample(favourityfood, 12)
        Food = []
        for item in foodrandom:
            food = db_dietcat.ShopFood.find_one({'商铺名称': item['菜品'].split("-")[0], '菜品': item['菜品'].split("-")[1]})
            food['id'] = food.get('_id').__str__()
            Food.append(food)
        return Food
    else:
        Food = []
        for item in favourityfood:
            food = db_dietcat.ShopFood.find_one({'商铺名称': item['菜品'].split("-")[0], '菜品': item['菜品'].split("-")[1]})
            food['id'] = food.get('_id').__str__()
            Food.append(food)
        randomfood = (FoodNotEnough(12 - len(Food)))
        for i in range(12 - len(Food)):
            food = db_dietcat.ShopFood.find_one(
                {'商铺名称': randomfood[i].split("-")[0], '菜品': randomfood[i].split("-")[1]})
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


def spoleep(userid, month):
    STime = []
    for item in day:
        T = month + item
        time = db_dietcat.UserData.find_one({'用户': userid, '时间': T})
        if time is None or time['睡眠时长'] is None:
            STime.append([0, 0, 0])
        elif (24 - int(time['睡眠时长']) - int(time['运动时长'])) > 0:
            STime.append([int(time['运动时长']), int(time['睡眠时长']), (24 - int(time['睡眠时长']) - int(time['运动时长']))])
        else:
            STime.append([0, 0, 0])
    return STime


def walkreport(userid, year):
    Walkdata = []
    for m in monthday:
        T = year + '-' + m
        walk = db_dietcat.UserData.find_one({'用户': userid, '时间': T})
        if walk is None or walk['步行距离'] is None:
            Walkdata.append(0)
        else:
            Walkdata.append(int(walk['步行距离']))
    return Walkdata


def weekspoleep(userid, now):
    STime = {}
    STime['sleep'] = []
    STime['sport'] = []
    STime['other'] = []
    weekday = []
    datestart = datetime.datetime.strptime(now, '%Y-%m-%d')
    while len(weekday) < 7:
        weekday.append(datestart.strftime('%Y-%m-%d'))
        datestart -= datetime.timedelta(days=1)
    weekday.reverse()
    for T in weekday:
        time = db_dietcat.UserData.find_one({'用户': userid, '时间': T})
        if time is None or time['睡眠时长'] is None:
            STime['sleep'].append(0)
            STime['sport'].append(0)
            STime['other'].append(0)
        elif (24 - int(time['睡眠时长']) - int(time['运动时长'])) > 0:
            STime['sleep'].append(int(time['睡眠时长']))
            STime['sport'].append(int(time['运动时长']))
            STime['other'].append(24 - int(time['睡眠时长']) - int(time['运动时长']))
        else:
            STime['sleep'].append(0)
            STime['sport'].append(0)
            STime['other'].append(0)
    return [STime['sport'], STime['sleep'], STime['other']]


def Week(now):
    weekday = []
    datestart = datetime.datetime.strptime(now, '%Y-%m-%d')
    while len(weekday) < 7:
        weekday.append(datestart.strftime('%m')+'月'+datestart.strftime('%d')+'日')
        datestart -= datetime.timedelta(days=1)
    weekday.reverse()
    return weekday

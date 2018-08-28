from pymongo import MongoClient
import pymongo
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



def RecommendList(list):
    RMDLIST=[]
    for i in list:
        RMDLIST.append(db_dietcat.ShopFood.find_one({'商铺名称':i.split("-")[0],'菜品':i.split("-")[1]}))
    return RMDLIST
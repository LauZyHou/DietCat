from pymongo import MongoClient
import pymongo

# 连接到MongoDB
conn = MongoClient('127.0.0.1', 27017)
# 获取dietcat这个DB对象
db_dietcat = conn.dietcat

# 检查用户名是否合法
def checkUserName(username):


# 向DB中添加一个用户
def addUser(username,password):

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 11:04:07 2018

@author: Durant
"""
import math
import numpy as np
import pymongo
from pymongo import MongoClient


def get_info():
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client['dietcat']
    posts = db.FoodEval
    users = []
    foods = []
    FoodEval = []
    scotts_posts = posts.find({}, {"_id": 0})
    for post in scotts_posts:
        u = len(users)
        f = len(foods)
        if not post['用户'] in users:
            users.append(post['用户'])
            u += 1
            FoodEval.append([0 for i in range(f)])
        if not post['菜品'] in foods:
            foods.append(post['菜品'])
            f += 1
            for i in range(u):
                FoodEval[i].append(0)
        FoodEval[users.index(post['用户'])][foods.index(post['菜品'])] = post['评分']
    #    print('FoodEval:\n',np.array(FoodEval))

    FoodSum = []
    b = np.transpose(FoodEval).tolist()
    for food in b:
        FoodSum.append(len(food) - food.count(0))
    print('FoodSum:', FoodSum)

    FoodEval_bk = np.array(FoodEval).tolist()
    UserFood = []
    for i in FoodEval_bk:
        n = []
        for j in i:
            if j > 0:
                n.append(i.index(j))
                i[i.index(j)] = 0
        UserFood.append(n)
    print('UserFood:', UserFood)

    FoodUser = []
    for i in b:
        n = []
        for j in i:
            if j > 0:
                n.append(i.index(j))
                i[i.index(j)] = 0
        FoodUser.append(n)
    print('FoodUser:', FoodUser)
    return users, foods, FoodEval, FoodSum, UserFood, FoodUser


def TOPK_Index(L, k=5):
    Index_list = []
    for x in sorted(L, reverse=True)[0:k]:
        Index_list.append(L.index(x))
        L[L.index(x)] = 0
    return Index_list


class FoodRMD:
    def __init__(self):
        self.users, self.foods, self.FoodEval, self.FoodSum, self.UserFood, self.FoodUser = get_info()
        self.UserNum = len(self.users)
        self.FoodNum = len(self.foods)
        #        self.Weight=np.zeros((self.FoodNum,self.FoodNum))
        self.weight()
        self.Recommand()

        print(self.FoodEval)

    def weight(self):
        a = np.zeros((self.FoodNum, self.FoodNum))
        for i in range(self.FoodNum):
            for j in self.FoodUser[i]:
                a[i][self.UserFood[j]] += 1
        for i in range(self.FoodNum):
            a[i][i] = 0
        #        print(a)
        Max = 0
        self.Weight = np.zeros((self.FoodNum, self.FoodNum))
        for i in range(self.FoodNum):
            for j in range(self.FoodNum):
                self.Weight[i][j] = a[i][j] / math.sqrt(self.FoodSum[i] * self.FoodSum[j])
                if Max < self.Weight[i][j]:
                    Max = self.Weight[i][j]
        for i in range(self.FoodNum):
            for j in range(self.FoodNum):
                self.Weight[i][j] = self.Weight[i][j] / Max

    def Recommand(self):
        self.P = np.zeros((self.UserNum, self.FoodNum))
        for UserID in range(self.UserNum):
            for FoodID in range(self.FoodNum):
                if FoodID in self.UserFood[UserID]:
                    continue
                else:
                    for k in self.UserFood[UserID]:
                        self.P[UserID][FoodID] += self.Weight[FoodID][k] * self.FoodEval[UserID][k]
                self.P[UserID][FoodID] = self.P[UserID][FoodID] / len(self.UserFood[UserID])

    #        print(P)

    def All_Recommand(self, K=3):
        p = self.P.tolist()
        for UserID in range(self.UserNum):
            print(self.users[UserID], [self.foods[i] for i in TOPK_Index(p[UserID], K)])

    def Single_Recommand(self, User, K=1):
        p = self.P.tolist()
        UserID = self.users.index(User)
        return [self.foods[i] for i in TOPK_Index(p[UserID], K)]

    def AddEval(self, User, Food, score=1):
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client['dietcat']
        posts = db.FoodEval
        post_data = {
            '用户': User,
            '菜品': Food,
            '评分': score,
        }
        result = posts.insert_one(post_data)
        print('One post: {0}'.format(result.inserted_id))
        if not User in self.users:
            self.users.append(User)
            self.FoodEval.append([0 for i in range(self.FoodNum)])
            self.UserFood.append([])
            self.UserNum = len(self.users)
        if not Food in self.foods:
            self.foods.append(Food)
            for i in range(self.UserNum):
                self.FoodEval[i].append(0)
            self.FoodSum.append(1)
            self.FoodUser.append([])
            self.FoodNum = len(self.foods)
        else:
            self.FoodSum[self.foods.index(Food)] += 1
        self.FoodEval[self.users.index(User)][self.foods.index(Food)] = score
        if not self.foods.index(Food) in self.UserFood[self.users.index(User)]:
            self.UserFood[self.users.index(User)].append(self.foods.index(Food))
        if not self.users.index(User) in self.FoodUser[self.foods.index(Food)]:
            self.FoodUser[self.foods.index(Food)].append(self.users.index(User))
        self.UserNum = len(self.users)
        self.FoodNum = len(self.foods)
        self.weight()
        self.Recommand()


RMD = FoodRMD()
print(RMD.users)
# print(RMD.Weight)
print(RMD.Single_Recommand('lzh', 10))
RMD.AddEval('Du', '食物20', 2)
RMD.AddEval('Du', '食物1', 5)
print(RMD.All_Recommand())
print(RMD.Single_Recommand('Du'))

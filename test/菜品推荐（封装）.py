# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 11:04:07 2018

@author: Durant
"""
import math
import numpy as np



def get_info():
    users=[]
    foods=[]
    f = open('用户菜品评价.csv')
    data=f.readlines()
    f.close()
    FoodEval=[]
    for line in data:
        u=len(users)
        f=len(foods)
        dataLine=line.split(",")
        if not dataLine[0] in users:
            users.append(dataLine[0])
            u+=1
            FoodEval.append([0 for i in range(f)])
        if not dataLine[1] in foods:
            foods.append(dataLine[1])
            f+=1
            for i in range(u):
                FoodEval[i].append(0)
        FoodEval[users.index(dataLine[0])][foods.index(dataLine[1])]=int(dataLine[2][:-1])
#    print('FoodEval:\n',np.array(FoodEval))
    
    FoodSum=[]
    b=np.transpose(FoodEval).tolist()
    for food in b:
        FoodSum.append(len(food)-food.count(0))
#    print('FoodSum:',FoodSum)
    
    FoodEval_bk=np.array(FoodEval).tolist()
    UserFood=[]
    for i in FoodEval_bk:
        n=[]
        for j in i :
            if j>0:
                n.append(i.index(j))
                i[i.index(j)]=0
        UserFood.append(n)
#    print('UserFood:',UserFood)

    FoodUser=[]
    for i in b:
        n=[]
        for j in i :
            if j>0:
                n.append(i.index(j))
                i[i.index(j)]=0
        FoodUser.append(n)
#    print('FoodUser:',FoodUser)
    return users,foods,np.array(FoodEval),FoodSum,UserFood,FoodUser

def TOPK_Index(L,k=5):
    Index_list=[]
    for x in sorted(L,reverse=True)[0:k]:
        Index_list.append(L.index(x))
        L[L.index(x)]=0
    return Index_list

class FoodRMD:
    def __init__(self):
        self.users,self.foods,self.FoodEval,self.FoodSum,self.UserFood,self.FoodUser=get_info()
        self.UserNum=len(self.users)
        self.FoodNum=len(self.foods)
        self.Weight=np.zeros((self.FoodNum,self.FoodNum))
        self.weight()
        print(self.FoodEval)
    def weight(self):
        a=np.zeros((self.FoodNum,self.FoodNum))
        for i in range(self.FoodNum):
            for j in self.FoodUser[i]:
                a[i][self.UserFood[j]]+=1
        for i in range(self.FoodNum):
            a[i][i]=0
#        print(a)
        Max=0
        self.Weight=np.zeros((self.FoodNum,self.FoodNum))
        for i in range(self.FoodNum):
            for j in range(self.FoodNum):
                self.Weight[i][j]=a[i][j]/math.sqrt(self.FoodSum[i]*self.FoodSum[j])
                if Max<self.Weight[i][j]:
                    Max=self.Weight[i][j]
        for i in range(self.FoodNum):
            for j in range(self.FoodNum):
                self.Weight[i][j]=self.Weight[i][j]/Max
    def Recommand(self,K):
        P=np.zeros((self.UserNum,self.FoodNum))
        for UserID in range(self.UserNum):
            for FoodID in range(self.FoodNum):
                if FoodID in self.UserFood[UserID]:
                    continue
                else:
                    for k in self.UserFood[UserID]:
                        P[UserID][FoodID]+=self.Weight[FoodID][k]*self.FoodEval[UserID][k]
                P[UserID][FoodID]=P[UserID][FoodID]/len(self.UserFood[UserID])
#        print(P)
        p=P.tolist()    
        for UserID in range(self.UserNum):
            print(self.users[UserID],[self.foods[i] for i in TOPK_Index(p[UserID],K)])    



RMD=FoodRMD()
#print(RMD.Weight)
RMD.Recommand(3)


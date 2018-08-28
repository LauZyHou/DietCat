from django.shortcuts import render
from django.shortcuts import HttpResponse
from mainapp import recommend as mainapp_RMD
from mainapp import dao as mainapp_dao
# 下载文件要用
from django.http import FileResponse

print('ajax')
global RMD
RMD = mainapp_RMD.FoodRMD()


# 提交用户反馈,这里用了ajax
# 其实我觉得在这个页面不用ajax也没什么,毕竟这个页面也没有别的需要交互的东西
def subProp(request):
    if request.method == 'POST':
        # 获得提交的具体内容
        msg = request.POST.get('prop')
        username = request.session.get('username')
        print('[ajax获取]', msg)
        # TODO 写入DB
        mainapp_dao.addDocInUser({'username': username, 'Discussion': msg})
        return HttpResponse('1')
    return HttpResponse('3')


# FIXME 提交某个用户对某个菜品的评分
def subScore(request):
    if request.method == 'POST':
        print(request.session)
        # 从Session中获取用户id
        userId = request.session.get('username')
        if userId is None:
            print('[error]session中没有获取到用户_id')
            return HttpResponse('3')
        print('[session获取]用户名是:', userId)
        # 获取提交的菜品的名称
        foodName = request.POST.get('foodName')
        print('[ajax获取]菜品的名称是:', foodName)
        # 获取提交的评分
        score = request.POST.get('score')
        print('[ajax获取]打分值:', score)
        # TODO 调用DAO写入数据库
        RMD.AddEval(userId, foodName, int(score))
        # TODO 影响训练模型
        RMD.AfferADD(userId, foodName, int(score))
        return HttpResponse('1')
    return HttpResponse('2')

from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.

# 用户登录
def getLoginPage(request):
    return render(request, r'web/login.html')


# 要去主页
def getIndexPage(request):
    return render(request, r'web/index.html', {'mylst': [1 for i in range(12)]})


# 用户要注销登录
def logOut(request):
    return render(request, r'web/login.html')


# 用户要进入账户资料页面
def getCntMsg(request):
    return render(request, r'web/cntmsg.html')


# 用户要进入身体信息页面
def getBdyMsg(request):
    return render(request, r'web/bdymsg.html')


# 用户要进入昨日打卡页面
def getPunchPage(request):
    return render(request, r'web/punch.html')


# 用户要进入一日三餐建议页面
def getMealsPage(request):
    return render(request, r'web/meals.html')


# 用户要进入设置页面
def getSettingPage(request):
    return render(request, r'web/setting.html')

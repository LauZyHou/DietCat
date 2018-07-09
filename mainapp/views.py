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

# 用户要进入就餐时间管理页面
def getTimePage(request):
    return render(request,r'web/time.html')

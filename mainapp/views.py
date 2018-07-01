from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.

# 用户登录
def getLoginPage(request):
    return render(request, r'web/login.html')


# 要去主页
def getIndexPage(request):
    return render(request, r'web/index.html', {'mylst': [1 for i in range(12)]})

from django.shortcuts import render
from django.shortcuts import HttpResponse
# 下载文件要用
from django.http import FileResponse


# Create your views here.

# 用户登录
def getLoginPage(request):
    return render(request, r'web/login.html')


# 用户要去主页(可能是登录操作,也可能就是单纯的页面切换操作)
def getIndexPage(request):
    # 看看Session里有没有,有就直接进不做校验
    print("从Session里检查")
    if request.session.get('loginId') is not None:
        print("Session校验成功")
        return render(request, r'web/index.html', {'mylst': [1 for i in range(12)]})
    elif request.method == 'POST':
        # 获取用户名和密码
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # FIXME 使用用户名和密码校验身份,并从DB中获取该用户id
        # 将登录身份存进session里
        request.session['loginId'] = 1234
        print("存进了Session里")
        return render(request, r'web/index.html', {'mylst': [1 for i in range(12)]})
    else:
        # 请先登录!
        return render(request, r'web/login.html')


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


# 用户要进入反馈页面
def getPropPage(request):
    return render(request, r'web/prop.html')


# 用户要进入食物推荐页面
def getRecommendPage(request):
    return render(request, r'web/recommend.html',
                  {'mylst': [1 for i in range(12)]
                      , 'pglst': [i + 1 for i in range(10)]})


# 用户要进入饮食计划页面
def getPlanPage(request):
    return render(request, r'web/plan.html')


# 测试下载报表文件
def testDown(request):
    file = open(r'test/测试报表文件.txt', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="mybb.txt"'
    return response


# 用户要进入某个具体的餐馆页面
def getEateryById(request, id):
    print("获得了餐馆的id", id)
    return render(request, r'web/detail/eatery.html')

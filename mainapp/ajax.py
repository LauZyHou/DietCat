from django.shortcuts import render
from django.shortcuts import HttpResponse
from mainapp import dao as mainapp_dao
from bson.objectid import ObjectId
from DietCat.settings import BASE_DIR
import os
from mainapp import recommend as mainapp_RMD

# 下载文件要用
from django.http import FileResponse

print('===ajax===')
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


# 更新账户信息
def updateMsg(request):
    # 检查是否是POST方式
    if request.method != 'POST':
        return HttpResponse('2')
    # 检查用户id
    userId = request.session.get('_id')
    if userId is None:
        return HttpResponse('3')
    # 获取提交的用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    print('username:', username, ',password:', password)
    # 检查字段缺失
    if username is None or password is None or \
            username == "" or password == "":
        return HttpResponse('4')
    # 检查密码长度
    if len(password) < 3:
        return HttpResponse('5')
    # 查询旧用户名,为了避免Session级别的bug污染该处,重新从数据库里查
    oldname = mainapp_dao.firstDocInUser({'_id': ObjectId(userId)}).get('username')
    if oldname is None:
        print('[debug]没能获取到旧用户名')
        return HttpResponse('-1')
    # 如果旧用户名和新用户名相同,可以直接修改密码
    if oldname == username:
        mainapp_dao.updateOneUser({'_id': ObjectId(userId)}, {'$set': {'password': password}})
        return HttpResponse('1')
    # 检查用户名占用情况,前面已经检查过了和自己的用户名不同
    if mainapp_dao.docCountInUser({"username": username}) > 0:
        return HttpResponse('6')
    # 所有的验证都通过,修改用户名和密码
    mainapp_dao.updateOneUser({'_id': ObjectId(userId)}, {'$set': {'username': username, 'password': password}})
    # 将修改后的用户名更新到Session里,因为可能修改失败,所以不能直接用username而是再从数据库里查一次
    request.session['username'] = mainapp_dao.firstDocInUser({'_id': ObjectId(userId)}).get('username')
    return HttpResponse('1')


# 上传头像
def uploadHead(request):
    # 校验提交方式
    if request.method != 'POST':
        return HttpResponse('2')
    # 检查用户id
    userId = request.session.get('_id')
    if userId is None:
        return HttpResponse('3')
    # 获取要上传的头像
    file_obj = request.FILES.get('file')
    # 检查是否没有选择文件
    if file_obj is None:
        return HttpResponse('4')
    # 上传头像(使用userId为名的jpg文件)
    with open(os.path.join(BASE_DIR, 'static', 'userpic', userId + '.jpg'), 'wb') as f:
        print(file_obj, type(file_obj))
        for chunk in file_obj.chunks():
            f.write(chunk)
    return HttpResponse('1')


# FIXME 删除本账户
def deleteMsg(request):
    # 校验提交方式
    #print('Hello!')
    if request.method != 'POST':
        return HttpResponse('2')
    # 检查用户id
    userId = request.session.get('_id')
    if userId is None:
        return HttpResponse('3')
    #print('wecan!')
    if os.path.isfile(BASE_DIR + '/static/userpic/' + userId +'.jpg'):
        os.remove(BASE_DIR + '/static/userpic/' + userId + '.jpg')
    mainapp_dao.deleteTheUser({'_id': ObjectId(userId)})
    request.session.flush()    #删除session
    # print("HelloWorld!")
    # TODO 根据id删除user表
    # TODO 删除头像
    # TODO 删除其它相关信息
    return HttpResponse('1')

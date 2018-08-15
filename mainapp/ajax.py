from django.shortcuts import render
from django.shortcuts import HttpResponse
# 下载文件要用
from django.http import FileResponse


# 提交用户反馈,这里用了ajax
# 其实我觉得在这个页面不用ajax也没什么,毕竟这个页面也没有别的需要交互的东西
def subProp(request):
    if request.method == 'POST':
        # 获得提交的具体内容
        msg = request.POST.get('prop')
        print(msg)
        # TODO 写入DB
        return HttpResponse('1')
    return HttpResponse('3')

from django import template

register = template.Library()


# 自定义过滤器做存在性测试
@register.filter(name='has')
def isIn(collection, arg):
    return arg in collection


# 注册自定义的过滤器,使能被模板语言找到
register.filter('has', isIn)

"""DietCat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp import views as mainapp_views
from mainapp import ajax as mainapp_ajax

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('firstuse/', mainapp_views.getLoginPage),
    path('index/', mainapp_views.getIndexPage),
    path('logout/', mainapp_views.logOut),
    path('cntmsg/', mainapp_views.getCntMsg),
    path('bdymsg/', mainapp_views.getBdyMsg),
    path('punch/', mainapp_views.getPunchPage),
    path('meals/', mainapp_views.getMealsPage),
    path('setting/', mainapp_views.getSettingPage),
    path('prop/', mainapp_views.getPropPage),
    path('recommend/', mainapp_views.getRecommendPage),
    path('plan/', mainapp_views.getPlanPage),
    path('testdown/', mainapp_views.testDown),
    path('eatery/<str:id>', mainapp_views.getEateryById),
    path('subprop/', mainapp_ajax.subProp),
    path('register/', mainapp_views.register),
    path('subscore/', mainapp_ajax.subScore),
    path('updatemsg/', mainapp_ajax.updateMsg),
    path('uploadhead/', mainapp_ajax.uploadHead),
]

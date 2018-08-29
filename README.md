# DietCat饮食专家
DietCat饮食推荐网站，Django工程，2018夏季课程项目。
## 小组成员
刘知昊，杜泽仁，郑海燕，段丽丽，顾河建。
## 主要界面展示
![](https://i.imgur.com/l9Hb1k5.jpg)

![](https://i.imgur.com/UP6Invh.jpg)

![](https://i.imgur.com/sRmOaFz.jpg)

![](https://i.imgur.com/QgHLlkT.jpg)

![](https://i.imgur.com/5Hcpflf.jpg)

![](https://i.imgur.com/o0SJUD8.jpg)

![](https://i.imgur.com/Fht3a0L.jpg)

![](https://i.imgur.com/nLwWrDq.jpg)

![](https://i.imgur.com/RIjt30f.jpg)

![](https://i.imgur.com/AzuWHxQ.jpg)

![](https://i.imgur.com/0YZb4Gh.jpg)
## 开发与合作日志
### 项目概况
为了大家快速上手开发本项目，这里我对整个工程做一个简要的概况描述。
#### 目录解读
【1】DietCat目录是与本项目同名的子目录，是Django项目的配置文件目录。
<br>
【2】mainapp目录是我创建的第一个app目录，如无特别需要，本项目使用这一个app足够。
<br>
【3】static目录是存放项目网页的依赖文件的，如js文件/css文件/图片等。
<br>
【4】templates目录是存放.html等网页结构文件的。
<br>
【5】test目录用于存放一些测试用的文件。
#### 快速开始
【1】配置文件目录中，settings.py是主配置文件，urls.py是url路由文件，wsgi.py是网络通信接口。
<br>
【2】templates目录中，直接在目录下的文件是用于继承的模板，extern目录我用来存放一些特殊页，web目录存放各大页面。
<br>
【3】static目录中，lzh目录是我写的依赖，其它是各个web框架的依赖。如各位需要大量重写网页样式，不妨建个自己的目录。
<br>
【4】数据备份到本项目目录：
<br>
mongodump.exe -h 127.0.0.1:27017 -d dietcat -o E:\WorkSpace\PyCharm\DietCat\test
<br>
【5】从备份的数据恢复：
<br>
mongorestore.exe -h 127.0.0.1:27017 -d dietcat E:\WorkSpace\PyCharm\DietCat\test\dietcat
<br>
【6】ML部分需要添加依赖:pandas,numpy,sklearn
<br>
【7】Django版本需要2.1,可使用cogitnda更新:
<br>
conda update -n 环境名(默认base) django
<br>
【8】为生成到本地数据库,单独运行test目录下形如Mongo*.py的文件。
#### 特别注意
在mainapp下的views.py中可以看到用户的各种操作，为了该文件的简洁，请在外面写后端操作的模块，封装成函数并在这里调用。
### 2018年7月2日
【1】简单完成了登录注册页，主页。
<br>
【2】添加了账户信息和身体信息页面。
<br>
【3】添加Echarts，新增每日打卡页面。
### 2018年7月9日
【1】添加了一日三餐页面。
<br>
【2】基本完成了所有功能页。
### 2018年8月14日
完善页面。
### 2018年8月22日
完成注册/登入/登出，添加DAO层，添加MongoDB数据库文件在test目录的子目录下。当数据库结构或内容发生重要改变时需要备份到此。
### 2018年8月29日
修复了主页不能显示菜品的bug，修复了菜品不能整齐排列的bug。

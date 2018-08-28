import pymongo
from pymongo import MongoClient


client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['dietcat']
posts = db.posts
'''
post_1 = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
post_2 = {
    'title': 'Virtual Environments',
    'content': 'Use virtual environments, you guys',
    'author': 'Scott'
}
post_3 = {
    'title': 'Learning Python',
    'content': 'Learn Python, it is easy',
    'author': 'Bill'
}

new_result = posts.insert_many([post_1, post_2, post_3])
print('Multiple posts: {0}'.format(new_result.inserted_ids))


scotts_posts = posts.find_one({'content': 'Le Python, it is easy','author': 'Bill'})
if scotts_posts is None:
    print(scotts_posts)
'''
i='掌上韩品（大华朗香园店）-韩式牛肉铁锅拌饭'
print(i.split("-")[1])

import pymongo
from pymongo import MongoClient
import datetime
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

scotts_posts = posts.find_one({'title': 'Virtual Environments',
    'content': 'Use virtual environments, you guys',
    'author': 'Scott'})

print(scotts_posts.get(['title','content']))
'''
serverDate = datetime.datetime.now().strftime('%Y-%m-%d')
print(serverDate.split('-')[1])



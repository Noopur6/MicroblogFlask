'''
Created on Apr 1, 2019

@author: NSNO
'''
from app import microblogapp,db,cli
from app.models import User,Post

@microblogapp.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post}
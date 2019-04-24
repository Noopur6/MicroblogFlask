'''
Created on Apr 1, 2019

@author: NSNO
'''
import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    #secret key to secure web app against CSRF
    SECRET_KEY = os.environ.get('SECRET KEY') or 'you-will-never-guess'
    #configurations for DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #configurations for mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['susantest38@gmail.com']
    POSTS_PER_PAGE=4
    LANGUAGES=['en','es']
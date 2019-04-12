from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login.login_manager import LoginManager
import logging
from logging.handlers import SMTPHandler

microblogapp = Flask(__name__)
microblogapp.config.from_object(Config)
db = SQLAlchemy(microblogapp)
migrate = Migrate(microblogapp, db)
login = LoginManager(microblogapp)
login.login_view = 'login' #view function that handles login

from app import routes, models, errors

if not microblogapp.debug and microblogapp.config['MAIL_SERVER']:
    auth = None
    if microblogapp.config['MAIL_USERNAME'] or microblogapp.config['MAIL_PASSWORD']:
        auth = (microblogapp.config['MAIL_SERVER'], microblogapp.config['MAIL_PASSWORD'])
    secure = None
    if microblogapp.config['MAIL_USE_TLS']:
        secure = ()
    mail_handler = SMTPHandler(mailhost=(microblogapp.config['MAIL_SERVER'], microblogapp.config['MAIL_PORT']), 
                               fromaddr='no-reply@'+microblogapp.config['MAIL_SERVER'], toaddrs=microblogapp.config['ADMINS'],
                               subject='Microblog failure', credentials=auth, secure=secure)
    mail_handler.setLevel(logging.ERROR)
    microblogapp.logger.addHandler(mail_handler)
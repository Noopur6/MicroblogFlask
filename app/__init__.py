from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login.login_manager import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

microblogapp = Flask(__name__)
microblogapp.config.from_object(Config)
db = SQLAlchemy(microblogapp)
migrate = Migrate(microblogapp, db)
login = LoginManager(microblogapp)
login.login_view = 'login' #view function that handles login and is redirected to whenever the request is unauthenticated
login.login_message = _l('Please login to access this page')
mail = Mail(microblogapp)
bootstrap = Bootstrap(microblogapp)
moment = Moment(microblogapp)
babel = Babel(microblogapp)

if not microblogapp.debug:
    #mail configuration
    if microblogapp.config['MAIL_SERVER']:
        auth = None
        if microblogapp.config['MAIL_USERNAME'] or microblogapp.config['MAIL_PASSWORD']:
            auth = (microblogapp.config['MAIL_USERNAME'], microblogapp.config['MAIL_PASSWORD'])
        secure = None
        if microblogapp.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(mailhost=(microblogapp.config['MAIL_SERVER'], microblogapp.config['MAIL_PORT']), 
                               fromaddr=microblogapp.config['MAIL_USERNAME'], toaddrs=microblogapp.config['ADMINS'],
                               subject='Microblog failure', credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        microblogapp.logger.addHandler(mail_handler)
        #fromaddr='no-reply@'+microblogapp.config['MAIL_SERVER']
        
    #file logger configuration
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    microblogapp.logger.addHandler(file_handler)
    microblogapp.logger.setLevel(logging.INFO)
    microblogapp.logger.info('Microblog startup')

@babel.localeselector    
def get_locale():
    return request.accept_languages.best_match(microblogapp.config['LANGUAGES'])

from app import routes, models, errors
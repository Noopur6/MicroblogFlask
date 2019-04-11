from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login.login_manager import LoginManager

microblogapp = Flask(__name__)
microblogapp.config.from_object(Config)
db = SQLAlchemy(microblogapp)
migrate = Migrate(microblogapp, db)
login = LoginManager(microblogapp)
login.login_view = 'login' #view function that handles login

from app import routes,models
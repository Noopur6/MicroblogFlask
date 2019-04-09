from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

microblogapp = Flask(__name__)
microblogapp.config.from_object(Config)
db = SQLAlchemy(microblogapp)
migrate = Migrate(microblogapp, db)

from app import routes,models
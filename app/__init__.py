from flask import (
    Flask
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

app = Flask(__name__)
app.config.from_object(config['default'])

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from app import views

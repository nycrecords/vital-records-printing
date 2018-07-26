from flask import (
    Flask
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
import boto3

app = Flask(__name__)
app.config.from_object(config['default'])

db = SQLAlchemy(app)
login_manager = LoginManager(app)
s3 = boto3.resource('s3')

from app import views

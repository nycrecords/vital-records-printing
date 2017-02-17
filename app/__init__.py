from flask import (
    Flask,
    render_template,
    flash,
    request,
    session
)

app = Flask(__name__)
# app.config.from_object('config')
app.config['DEBUG'] = True

from app import views

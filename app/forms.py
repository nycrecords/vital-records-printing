from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class SearchForm(FlaskForm):
    name = StringField("name", validators=[Required()])
    submit = SubmitField("submit")

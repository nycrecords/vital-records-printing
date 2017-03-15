from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import Length, NumberRange, Optional


class SearchForm(FlaskForm):
    type = SelectField("Type of Certificate", choices=[('birth', 'Birth'), ('death', 'Death'), ('marriage', 'Marriage')])
    county = SelectField("County", choices=[('kings', 'Brooklyn'), ('queens', 'Queens'), ('bronx', 'Bronx'), ('manhattan', 'Manhattan'),
                                            ('richmond', 'Staten Island')])
    year = IntegerField("Year", validators=[NumberRange(min=0, max=9999), Optional()])
    number = StringField("Certificate Number")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    soundex = StringField("Soundex", validators=[Length(max=4)])
    # name = StringField("name", validators=[Required()])
    submit = SubmitField("submit")

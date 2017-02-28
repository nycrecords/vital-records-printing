from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import Length


class SearchForm(FlaskForm):
	type = SelectField("Type of Certificate", choices=[('b', 'Birth'),('d', 'Death'),('m', 'Marriage')])
	county = SelectField("County", choices=[('k', 'Brooklyn'),('q', 'Queens'),('b', 'Bronx'),('m', 'Manhattan'),('r', 'Staten Island')])
	year = IntegerField("Year")
	number = IntegerField("Certificate Number")
	first_name = StringField("First Name")
	last_name = StringField("Last Name")
	soundex = StringField("Soundex", validators=[Length(max=4)])
	# name = StringField("name", validators=[Required()])
	submit = SubmitField("submit")

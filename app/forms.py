from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import Length, NumberRange, Optional


class SelectSortField(SelectField):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            choices=[('none', 'None'), ('asc', 'Ascending'), ('desc', 'Descending')],
            **kwargs)


class SearchForm(FlaskForm):
    # visible inputs
    type = SelectField("Type of Certificate", choices=[('birth', 'Birth'), ('death', 'Death'), ('marriage', 'Marriage')])
    county = SelectField("County", choices=[('kings', 'Brooklyn'), ('queens', 'Queens'), ('bronx', 'Bronx'), ('manhattan', 'Manhattan'),
                                            ('richmond', 'Staten Island')])
    year = IntegerField("Year", validators=[NumberRange(min=0, max=9999), Optional()])
    number = StringField("Certificate Number")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    soundex = StringField("Soundex", validators=[Length(max=4)])

    submit = SubmitField("Submit")

    # hidden inputs
    year_sort = SelectSortField("Year")
    number_sort = SelectSortField("Certificate Number")
    first_name_sort = SelectSortField("First Name")
    last_name_sort = SelectSortField("Last Name")
    soundex_sort = SelectSortField("Soundex")
    start = IntegerField("Start", default=0)

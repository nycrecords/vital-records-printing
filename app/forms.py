from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import Length


class Form(FlaskForm):
    class Meta:
        def bind_field(self, form, unbound_field, options):
            """
            Strip field values of whitespace.
            http://stackoverflow.com/questions/26232165/automatically-strip-all-values-in-wtforms
            """
            filters = unbound_field.kwargs.get('filters', [])
            filters.append(_strip_filter)
            return unbound_field.bind(form=form, filters=filters, **options)


def _strip_filter(value):
    """
    Call strip() on given value if possible.
    :return: stripped or unaltered value
    """
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value


class SelectSortField(SelectField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            choices=[('none', 'None'), ('asc', 'Ascending'), ('desc', 'Descending')],
            **kwargs)


class SearchForm(Form):
    """
    All text inputs are StringFields because they accept wildcards ("*")
    """
    # visible inputs
    type = SelectField(
        "Type of Certificate",
        choices=[
            ('birth', 'Birth'),
            ('death', 'Death'),
            ('marriage', 'Marriage')
        ])
    county = SelectField(
        "County",
        choices=[
            ('', 'All'),
            ('kings', 'Kings / Brooklyn'),
            ('queens', 'Queens'),
            ('bronx', 'Bronx'),
            ('manhattan', 'Manhattan'),
            ('richmond', 'Richmond / Staten Island')
        ])
    year = StringField("Year", validators=[Length(max=4)])
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


class LoginForm(Form):
    pass

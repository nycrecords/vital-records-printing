import string
from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SubmitField,
    SelectField,
    IntegerField,
    PasswordField,
    BooleanField,
    TextAreaField,
)
from wtforms.validators import Length, DataRequired
from flask_login import current_user

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
    username = StringField("Username")
    password = PasswordField("Password")
    remember = BooleanField("Remember me")


class PasswordForm(Form):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[Length(min=8, max=32)])

    def validate(self):
        base_validation = super().validate()
        is_valid_current_password = current_user.check_password(self.current_password.data)
        is_valid_new_password = current_user.is_new_password(self.new_password.data)
        specials = set(string.punctuation)
        has_num = any(c.isdigit() for c in self.new_password.data)
        has_upper = any(c.isupper() for c in self.new_password.data)
        has_lower = any(c.islower() for c in self.new_password.data)
        has_special = any(c in specials for c in self.new_password.data)

        if not has_num:
            self.new_password.errors.append("Your new password must contain at least 1 number.")
        if not has_upper:
            self.new_password.errors.append("Your new password must contain at least 1 capital letter.")
        if not has_lower:
            self.new_password.errors.append("Your new password must contain at least 1 lower case letter.")
        if not has_special:
            self.new_password.errors.append("Your new password must contain at least 1 special character.")

        if not is_valid_new_password:
            self.new_password.errors.append(
                "Your new password cannot be the same as your current password or your last 3 passwords.")
        if not is_valid_current_password:
            self.current_password.errors.append("Incorrect password.")

        return (
            base_validation and
            is_valid_current_password and
            is_valid_new_password and
            has_num and
            has_upper and
            has_lower and
            has_special
        )


class ReportForm(Form):
    """
    Form for reporting an issue with a certificate
    """
    county = StringField()
    month = StringField()
    day = StringField()
    year = StringField()
    age = StringField()
    number = StringField()
    soundex = StringField()
    first_name = StringField()
    last_name = StringField()
    comments = TextAreaField()
    submit = SubmitField()

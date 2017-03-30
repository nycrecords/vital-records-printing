"""
Models for Vital Records Printing
"""

from app import db
from app.constants import (
    certificate_types,
    months,
    counties
)
from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime

counter = 0

class Cert(db.Model):
    """
    Define the Cert class with the following columns:

    type - an enum containing certificate type (e.g. 'birth')
    county - an enum containing one of 'brooklyn', 'queens', 'bronx', 'manhattan', 'staten_island'
    year - an int (4) containing certificate year
    number - a varchar containing certificate number
    first_name - a varchar containing first name of individual pertaining to certificate
    last_name - a varchar containing last name of individual pertaining to certificate
    soundex - a varchar(4) containing ???
    filename - a varchar containing filename
    """
    __tablename__ = "certificate"
    id = db.Column(db.Integer, primary_key=True)  # TODO: might have use composite key instead (names & certificate number)
    # TODO: type of marriage change to 'bride' and 'groom'?
    type = db.Column(
        db.Enum(
            certificate_types.BIRTH,
            certificate_types.DEATH,
            certificate_types.MARRIAGE,
            name='certificate_type'),
        nullable=False
    )
    county = db.Column(
        db.Enum(
            counties.KINGS,
            counties.QUEENS,
            counties.BRONX,
            counties.MANHATTAN,
            counties.RICHMOND,
            name='county'),
        nullable=False
    )
    month = db.Column(
        db.Enum(
            months.JAN,
            months.FEB,
            months.MAR,
            months.APR,
            months.MAY,
            months.JUN,
            months.JUL,
            months.AUG,
            months.SEP,
            months.OCT,
            months.NOV,
            months.DEC,
            name='month'))
    # TODO: on day, year, and number: http://stackoverflow.com/questions/20810134/why-unsigned-integer-is-not-available-in-postgresql
    day = db.Column(db.String(6))  # some include apostrophes, why?
    year = db.Column(db.Integer, nullable=False)
    number = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64))  # many first names not included
    last_name = db.Column(db.String(64), nullable=False)
    soundex = db.Column(db.String(4))  # NULLABLE?!
    filename = db.Column(db.String(64), nullable=False)

    def __init__(self,
                 type,
                 county,
                 year,
                 number,
                 first_name,
                 last_name,
                 soundex,
                 filename=None):
        self.type = type
        self.county = county
        self.year = year
        self.number = number
        self.first_name = first_name
        self.last_name = last_name
        self.soundex = soundex
        self.filename = filename

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name) \
            if self.first_name is not None else self.last_name


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(65), unique=True)
    password = db.Column(db.String(256))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    date_pass_changed = db.Column(db.DateTime())
    previous_passwords = db.Column(db.ARRAY(db.String(256)))  # TODO: MAX_PREVIOUS_PASSWORDS = 3

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.set_password(password, commit=True)
        self.first_name = first_name
        self.last_name = last_name

    def set_password(self, password, commit=False):
        # Update the date_pass_changed
        self.date_pass_changed = datetime.now()
        # Set the new password
        self.password = generate_password_hash(password)
        # Store password in previous_passwords array
        if self.previous_passwords is None:
            # counter+=1
            # self.previous_passwords = [str(counter) + ',' + self.password]
            self.previous_passwords = [self.password]
        else:
            # size = 0
            # for old_pass in self.previous_passwords:
            #     size += 1
            # if size < 3:
            #     # self.previous_passwords.append(str(counter) + ',' + self.password)
            #     self.previous_passwords.append(self.password)
            #     flag_modified(self, 'previous_passwords')
            # else:  # size >=3
            #     pass
            self.previous_passwords.append(self.password)
            flag_modified(self, 'previous_passwords')

        if commit:
            db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

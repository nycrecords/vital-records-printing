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
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(64))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

"""
Models for Vital Records Printing
"""

import os
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
from datetime import datetime, timedelta


class Cert(db.Model):
    """
    Define the Cert class for the `certificate` table with the following columns:

    id          integer, primary key
    type        certificate_type, type of certificate (e.g. "birth")
    county      county, certificate county (e.g. "queens")
    month       month, month certificate was issued (e.g. "jan")
    day         varchar(10), day certificate was issued
    year        integer, year certificate was issued
    number      varchar(10), certificate number
    first_name  varchar(50), first name of individual pertaining to the certificate
    last_name   varchar(50), last name of individual pertaining to the certificate
    age         varchar(10), age of individual pertaining to the certificate
    soundex     varchar(4), certificate soundex
    file_id     integer, foreign key to `file`
    
    To create the indexes for the `certificate` table, use the "create_certificate_indexes" 
    manager command. This command will create 64 indexes which will make make READing/SELECTing 
    and, by extension, searching for certificates fast given the inputs (columns) available on the
    search form, but will come at the cost of slow WRITEs (INSERTs, UPDATEs, and DELETEs).
    For this reason, indexes have not been included in this model and it is probably a good idea 
    to postpone index creation until after initial population (the access-to-postgresql transfer)
    has been completed.
    
    MISC: 
        The structure of this table is largely determined by a preexisting, 
        poorly-designed Access databases. 
        - Here are some examples of `age` field values that are persisted in this 
          database: "15 y", "9 m". A better way of handling this (if it were worth it)
          would be to use two columns: `age` (integer) and `age_unit` (varchar).
        - The `day` column is of type varchar instead of integer. Why? Here is an example 
          of existing day data: "21'15". What the significance of the apostrophe is and 
          why it is included in only some records is something we may never truly know.
          I suspect what is on the lhs of the apostrophe is the hour of that day.
        
    """
    __tablename__ = "certificate"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(*certificate_types.ALL, name='certificate_type'), nullable=False)
    county = db.Column(db.Enum(*counties.ALL, name='county'), nullable=False)
    month = db.Column(db.Enum(*months.ALL, name='month'))
    day = db.Column(db.String(10))
    year = db.Column(db.Integer)
    number = db.Column(db.String(10))  # there are many brides without certificate numbers
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64), nullable=False)
    age = db.Column(db.String(10))
    soundex = db.Column(db.String(4))
    file_id = db.Column(db.Integer, db.ForeignKey("file.id"))

    file = db.relationship("File", backref=db.backref("certificate", uselist=False))

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name) \
            if self.first_name is not None else self.last_name


class File(db.Model):
    """
    Define the File class for the `file` table with the following columns:

    id          integer, primary key
    name        varchar, name of certificate PDF file
    path        varchar, path to where file is located
    converted   boolean, has the PDF file been converted to PNG(s)?

    """
    __tablename__ = "file"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    path = db.Column(db.String(256), unique=True)
    converted = db.Column(db.Boolean, default=False)

    @property
    def file_path(self):
        return os.path.join(self.path, self.name)

    @property
    def pngs(self):
        if not self.converted:
            self.convert()
        return [png for png in png_dir]  # TODO

    def convert(self):
        # TODO: try, and call conversion function here
        self.converted = True
        db.commit()
        return self.pngs


class User(db.Model, UserMixin):  # TODO: write tests for this
    """
    Define the User class for the `user` table with the following columns:
    
    id                  integer, primary key
    username            varchar(65), human-readable user identifier
    first_name          varchar(64), user's first name
    last_name           varchar(64), user's last name
    expiration_date     datetime, timestamp of when user's password will expire
    
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(65), unique=True)
    password = db.Column(db.String(256))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    expiration_date = db.Column(db.DateTime())

    history = db.relationship("History", backref="user", lazy="dynamic")

    MAX_PREV_PASS = 3  # number of previous passwords to check against
    DAYS_UNTIL_EXPIRATION = 90  # number of days until password expires

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.set_password(password, update_history=False)  # only update on password resets
        self.first_name = first_name
        self.last_name = last_name

    def is_new_password(self, password):
        """
        Returns whether the supplied password is not the same as the current 
        or previous passwords (True) or not (False). 
        """
        existing_passwords = list(filter(None, [self.password] + [h.password for h in self.history.all()]))
        return not existing_passwords or all(not check_password_hash(p, password) for p in existing_passwords)

    def set_password(self, password, update_history=True):
        if self.is_new_password(password):
            if update_history:
                # update previous passwords
                if self.history.count() >= self.MAX_PREV_PASS:
                    # remove oldest password
                    self.history.filter_by(  # can't call delete() when using order_by()
                        id=self.history.order_by(History.timestamp.asc()).first().id
                    ).delete()
                db.session.add(History(self.id, self.password))

            self.expiration_date = datetime.utcnow() + timedelta(days=self.DAYS_UNTIL_EXPIRATION)
            self.password = generate_password_hash(password)

            db.session.commit()

    def update_password(self, current_password, new_password):
        if self.check_password(current_password):
            self.set_password(new_password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class History(db.Model):
    """
    Define the History class for the `history` table with the following columns:
    
    id          integer, primary key
    user_id     integer, foreign key to `users`
    timestamp   datetime, time when record created
    password    varchar(256), hashed password
    
    """
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime)
    password = db.Column(db.String(256))

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
        self.timestamp = datetime.utcnow()

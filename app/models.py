"""
Models for Vital Records Printing
"""

import os
from app import db
from app.constants import certificate_types, months, counties


class Cert(db.Model):
    """
    Define the Cert class for the `certificate` table with the following columns
    and indices:

    id          integer, primary key
    type        enum, type of certificate (e.g. "birth")
    county      enum, certificate county (e.g. "queens")
    month       enum, month certificate was issued (e.g. "jan")
    day         varchar(10), day certificate was issued
    year        integer, year certificate was issued
    number      varchar(10), certificate number
    first_name  varchar(50), first name of individual pertaining to the certificate
    last_name   varchar(50), last name of individual pertaining to the certificate
    age         varchar(10), age of individual pertaining to the certificate
    soundex     varchar(4), certificate soundex
    file_id     integer, foreign key to File
    
    idx_year_county_type        year, county, type
    idx_first_county_type       first_name, county, type
    idx_last_county_type        last_name, county, type
    idx_soundex_county_type     soundex, county, type
    idx_number_county_type      number, county, type
    
    This high amount of indices will make READing/SELECTing and, by extension, 
    searching for certificates fast given the inputs (columns) available on the
    search form, but will come at the cost of slow WRITEs (INSERTs, UPDATEs, and DELETEs).
    Therefore, it is probably a good idea to postpone index creation until after the
    the access-to-postgresql transfer has completed. This means you should comment out 
    the __table_args__ below and, after initial population, run 
    `python manage.py create_certificate_indices`.
    
    MISC: 
        The structure of this table is largely determined by a preexisting, 
        poorly-designed Access databases. 
        - Here are some examples of `age` field values that are persisted in this 
          database: "15 y", "9 m". A better way of handling this (if it were worth it)
          would be to use two columns: `age` (integer) and `age_unit` (varchar).
        - The `day` column is of type varchar instead of integer. Why? Here is an example 
          of existing day data: "21'15". What is the significance of the apostrophe and 
          why is it included in only some records is something we may never truly know.
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

    __table_args__ = (
        db.Index("idx_year_county_type", "year", "county", "type"),
        db.Index("idx_first_county_type", "first_name", "county", "type"),
        db.Index("idx_last_county_type", "last_name", "county", "type"),
        db.Index("idx_soundex_county_type", "soundex", "county", "type"),
        db.Index("idx_number_county_type", "number", "county", "type"),
        # TODO: more combos!
    )

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

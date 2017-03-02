"""
Models for Vital Records Printing
"""

from app import db


class Certificate(db.Model):
    """
    Define the Certificate class with the following columns:

    type - an enum containing certificate type (e.g. 'birth')
    county - an enum containing one of 'brooklyn', 'queens', 'bronx', 'manhattan', 'staten_island'
    year - an int (4) containing certificate year
    number - an int containing certificate number
    first_name - a varchar containing first name of individual pertaining to certificate
    last_name - a varchar containing last name of individual pertaining to certificate
    soundex - a varchar(4) containing ???
    filename - a varchar containing filename
    """
    __tablename__ = "certificate"
    # id=primary key
    type = db.Column(  # TODO: type of marriage too (bride vs groom)
        db.Enum(
            'Birth',
            'Death',
            'Marriage',
            name='certificate_type'),
        nullable=False)
    county = db.Column(
        db.Enum(
            'Kings',
            'Queens',
            'Bronx',
            'Manhattan',
            'Staten_Island',
            name='county'))
    year = db.Column(db.Integer)  # TODO: limit to 4 digits, unsigned
    number = db.Column(db.Integer)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    soundex = db.Column(db.String(4))
    filename = db.Column(db.String(64))

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

import os
from dotenv.main import load_dotenv
from flask import url_for

BASEDIR = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(BASEDIR, '.env')
load_dotenv(dotenv_path)


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY") or "ssshhhhh"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or 'postgresql://vital_records_printing_db@127.0.0.1:5432/vital_records_printing_v2'

    # suppress warning
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # location of certificate image directory from within static folder (default: "img/certificate")
    CERT_IMAGE_STATIC_DIRECTORY = os.environ.get('CERT_IMAGE_STATIC_DIRECTORY') or \
                                  os.path.join("img", "certificate")

    # absolute path to mounted certificate image directory (".../app/static/img/certificate")
    CERT_IMAGE_DIRECTORY = os.path.join(BASEDIR, "app", "static", CERT_IMAGE_STATIC_DIRECTORY)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    pass


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}

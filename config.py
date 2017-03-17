import os
from dotenv.main import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)

class Config(object):
    DEBUG = True
    SECRET_KEY = "secrets"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://vital_records_printing_db@10.0.0.2:5432/vital_records_printing'  # TODO: vagrant->actual user
    OUTPUT_FILE_PATH = os.environ.get('OUTPUT_FILE_PATH') or "app/png/"


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    pass


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}

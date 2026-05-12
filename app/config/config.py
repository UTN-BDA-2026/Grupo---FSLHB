from dotenv import load_dotenv
from pathlib import Path
import os

basedir = os.path.abspath(Path(__file__).parents[2])
env_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path=env_path)

class Config(object):
    TESTING = False
    HASHIDS_MIN_LENGTH: str = os.environ.get('HASHIDS_MIN_LENGTH') or '8'
    HASHIDS_ALPHABET: str = os.environ.get('HASHIDS_ALPHABET') or os.environ.get('ALFABETO') or 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    HASHIDS_SALT: str = os.environ.get('HASHIDS_SALT') or 'default_salt'
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'default_secret_key'

    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/hockey_test'

class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/hockey_dev'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/hockey'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

def factory(app: str) -> Config:
    configuration = {
        'testing': TestConfig,
        'development': DevelopmentConfig,
        'production': ProductionConfig
    }

    return configuration[app]

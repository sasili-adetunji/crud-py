import os

basedir = os.path.abspath(os.path.dirname(__file__))

develop_database = "sqlite:///" + basedir \
                              + "crud_db.sqlite"
test_database = "sqlite:///" + basedir \
                              + "test_db.sqlite"

class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', b"\xdb'\xf8\xc3h\n\xf2\x8d9#\xad\xf2\xc2Tv\x89\x96\xe2\xfe\xdb#\xf8\\\x05")


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = develop_database
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = test_database

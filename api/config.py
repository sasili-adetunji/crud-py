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


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = develop_database


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = test_database

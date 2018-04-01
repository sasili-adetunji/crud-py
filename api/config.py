import os

basedir = os.path.abspath(os.path.dirname(__file__))

develop_database = "sqlite:///" + basedir \
                              + "/api/dev_db.sqlite"
test_database = "sqlite:///" + basedir \
                              + "/test/test_db.sqlite"

class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    DEVELOP_DATABASE = develop_database


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    TESTING_DATABASE = test_database

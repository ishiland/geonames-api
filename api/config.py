import os


class BaseConfig(object):
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_TEST')
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os
from flask import current_app
from flask_testing import TestCase
from api import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertEqual(app.config['SECRET_KEY'], os.environ.get('SECRET_KEY'))
        self.assertFalse(current_app is None)
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], os.environ.get('DATABASE_URL'))


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertEqual(app.config['SECRET_KEY'], os.environ.get('SECRET_KEY'))
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], os.environ.get('DATABASE_URL_TEST'))


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])

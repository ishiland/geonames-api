from flask_testing import TestCase
from api import create_app, db
from manage import load_geonames, load_admin1_codes, load_admin2_codes


class BaseTestCase(TestCase):

    def load_test_data(self):
        load_admin1_codes('tests/data/admin1CodesASCII.txt', self.app.config['SQLALCHEMY_DATABASE_URI'])
        load_admin2_codes('tests/data/admin2Codes.txt', self.app.config['SQLALCHEMY_DATABASE_URI'])
        load_geonames('tests/data/cities.txt', self.app.config['SQLALCHEMY_DATABASE_URI'])

    @classmethod
    def create_app(cls):
        app = create_app()
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        self.load_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging


basedir = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO, filename='geonames-api.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d, %H:%M:%S')


# instantiate the extensions
db = SQLAlchemy()
cors = CORS()


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app)

    from api.views import geonames_blueprint
    app.register_blueprint(geonames_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app

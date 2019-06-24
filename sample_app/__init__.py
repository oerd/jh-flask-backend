from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from config import config

from logging.config import dictConfig

dictConfig({  # configure logging & log format
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
bc = Bcrypt()
cors = CORS()


def create_app(config_name='default'):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # create and init DB
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # create and init JWT
    jwt.init_app(app)

    # create and init Bcrypt
    bc.init_app(app)

    # fix CORS
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # register blueprints
    from .users import bp as places_blueprint
    app.register_blueprint(places_blueprint, url_prefix="/users")

    # a default page that says hello
    @app.route('/hi/<name>')
    def hi_name(name):
        return 'Hello, {}!'.format(name)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # a default page that says hello
    @app.route('/')
    def hi():
        return 'Hello, Root!'

    return app

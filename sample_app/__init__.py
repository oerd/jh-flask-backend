from flask import Flask, jsonify
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
    from .users import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    from .entities import BankAccountItemsApi
    app.add_url_rule("/api/bank-accounts/<int:entity>", view_func=BankAccountItemsApi.as_view("account_items_api"))

    from .entities import BankAccountsApi
    app.add_url_rule("/api/bank-accounts", view_func=BankAccountsApi.as_view("accounts_api"))

    from .entities import OperationItemsApi
    app.add_url_rule("/api/operations/<int:entity>", view_func=OperationItemsApi.as_view("operation_items_api"))

    from .entities import OperationsApi
    app.add_url_rule("/api/operations", view_func=OperationsApi.as_view("operations_api"))

    from .entities import LabelItemsApi
    app.add_url_rule("/api/labels/<int:entity>", view_func=LabelItemsApi.as_view("label_items_api"))

    from .entities import LabelsApi
    app.add_url_rule("/api/labels", view_func=LabelsApi.as_view("labels_api"))

    from .authenticate import authentication_bp
    app.register_blueprint(authentication_bp, url_prefix="/api")

    # a heartbeat, is very comfortable to have
    @app.route("/heartbeat")
    def heartbeat():
        return jsonify({"status": "healthy"})

    # a default page that says hello with name
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

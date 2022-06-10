from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth
        from .assets import compile_static_assets

        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        db.create_all()

        if app.config['FLASK_ENV'] == 'development':
            compile_static_assets(app)

        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        MAIL_PORT = 465
        MAIL_USE_SSL = True
        MAIL_USERNAME = "iyerarchith@gmail.com"
        MAIL_PASSWORD = "zethesavage"
        MAIL_DOMAIN = 'gmail.com'
        MAIL_ENABLE_STARTTLS_AUTO = True

        return app


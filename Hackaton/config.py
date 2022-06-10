import os


class Config:
    """Set Flask config variables."""

    SECRET_KEY = os.urandom(32)

    FLASK_ENV = 'development'
    TESTING = True

    # TEMPLATES_FOLDER = 'templates'

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:////Users/archith/PycharmProjects/BackEndScraping/venv/Hackaton/Project/db.db"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "iyerarchith@gmail.com"
    MAIL_PASSWORD = "zethesavage"
    MAIL_DOMAIN = 'gmail.com'
    MAIL_ENABLE_STARTTLS_AUTO = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GEOIPIFY_API_KEY = 'at_tN2hag8ZSQdks2Hmy2MJgz519GD4n'


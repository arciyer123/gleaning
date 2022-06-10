from . import db
from . import login_manager
from flask import render_template
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from time import time
import jwt
from flask_mail import Message
from . import mail
from flask_sqlalchemy import SQLAlchemy

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)


def send_email(user):

    token =get_reset_token(user)

    msg = Message()
    msg.subject = "Flask App Password Reset"
    msg.sender =('Glean', 'mairajuble@gmail.com')
    msg.recipients = [user.email]
    msg.html = render_template('reset_email.html', user=user, token=token)

    mail.send(msg)


def c_send_email(c_user):

    token =get_reset_token(c_user)

    msg = Message()
    msg.subject = "Flask App Password Reset"
    msg.sender =('Glean', 'mairajuble@gmail.com')
    msg.recipients = [c_user.email]
    msg.html = render_template('c_reset_email.html', user=c_user, token=token)

    mail.send(msg)


def get_reset_token(self, expires=500):
    return jwt.encode({'reset_password': self.name,
                       'exp': time() + expires},
                      key=str(os.getenv('SECRET_KEY')))


##### password reset for farmer ###########

def verify_reset_token(token):
    try:
        name= jwt.decode(token,key=str(os.getenv('SECRET_KEY_FLASK')))['reset_password']
    except Exception as e:
        print (e)
        return
    return User.query.filter_by(name=name).first()

  ########## Password reset for customer ######
def verify_reset_token_customer(token):
    try:
        name= jwt.decode(token,key=str(os.getenv('SECRET_KEY_FLASK')))['reset_password']
    except Exception as e:
        print (e)
        return
    return Customer.query.filter_by(name=name).first()


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'flasklogin-users'
    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(100),
                     nullable=False,
                     unique=False)

    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)

    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)


    farmName = db.Column(db.String(100),
                        index=False,
                        unique=False,
                        nullable=False)

    farmType = db.Column(db.String(60),
                        index=False,
                        unique=False,
                        nullable=False)


    address = db.Column(db.String(100),
                        index=False,
                        unique=True,
                        nullable=False)

    location = db.Column(db.String(100),
                        index=False,
                        unique=True,
                        nullable=False)


    created_on = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)

    last_login = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)


    def set_password(self, password):
        """Create hashed password."""
        print ("done")
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Event(db.Model):
    __tablename__ = 'events'
    # __bind_key__ = 'db2'

    id = db.Column(db.Integer,
                   primary_key=True)

    date = db.Column(db.DateTime(),
                     nullable=False,
                     unique=False)

    email = db.Column(db.String(100),unique=True,nullable=False)

    time = db.Column(db.String(40),
                      unique=False,
                      nullable=False)


    cap =  db.Column(db.String(100),
                     nullable=False,
                     unique=False)
    signedUp = db.Column(db.String(100),
                     nullable=False,
                     unique=False)

    pricePerPound = db.Column(db.String(100),
                     nullable=False,
                     unique=False)

    location = db.Column(db.String(100),
                     nullable=False,
                     unique=False)

    farmName = db.Column(db.String(100),
                        index=False,
                        unique=False,
                        nullable=False)

    farmType = db.Column(db.String(60),
                        index=False,
                        unique=False,
                        nullable=False)

    address = db.Column(db.String(100),
                        index=False,
                        unique=True,
                        nullable=False)

class Customer(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'flasklogin-customers'
    # __bind_key__ = 'db3'

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(100),
                     nullable=False,
                     unique=False)

    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)

    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)


    created_on = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)

    last_login = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)


    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)

from flask import Flask
from flask import redirect, render_template, flash, Blueprint, request, url_for,session
from flask_login import current_user, login_user,login_required
from Project.forms import SignupForm,CustomerSignupForm,CustomerLoginForm,LoginForm
from Project.models import db, User, Customer,Event
from .import login_manager
from sqlalchemy import exc
from flask_mail import Mail, Message
from . import mail
from werkzeug.utils import secure_filename
import os
from datetime import date , datetime
from threading import Thread

# Blueprint Configuration
app = Flask(__name__, instance_relative_config=False)
mail.init_app(app)
login_manager.init_app(app)

auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')
dirt = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = dirt + '/static/Uploads/'

def send_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_message(msg):
    pass


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Sign-up form to create new user accounts.
    GET: Serve sign-up page.
    POST: Validate form, create account, redirect user to dashboard.
    """
    form = SignupForm()
    if form.is_submitted():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(name=form.name.data,
                        email=form.email.data,
                        farmName = form.farmName.data,
                        farmType = form.farmType.data,
                        address = form.address.data,
                        location = form.address.data + '' + str(form.zip.data),
                        created_on=date.today(),
                        last_login=datetime.now()
                        )
            user.set_password(form.password.data)
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER,filename))
            reciever = form.email.data
            print(reciever)
            rec = []
            rec.append(reciever)
            print(rec)

            db.session.add(user)
            db.session.commit()


            msg = Message("Registration",
                         sender=("GoGlean","iyerarchith@gmail.com"),
                         recipients=rec,
                         body='<h3>Thanks for registering with GoGlean!</h3>'
                         )


            Thread(target=send_email, args=(app, msg)).start()
            # this will send message to new registerd person



            login_user(user)  # Log in as newly created user
            return redirect(url_for('main_bp.cover'))
        flash('A user already exists with that email address.')
    return render_template('signup.jinja2.html',
                           title='Create an Account.',
                           form=form,
                           template='signup-page',
                           body="Sign up for a user account.")



@auth_bp.route('/main_dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    # result = Event.query.filter_by(email = current_user.email).all()
    return render_template("dashboard.jinja2.html")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.
    GET: Serve Log-in page.
    POST: Validate form and redirect user to dashboard.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))  # Bypass if user is logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Validate Login Attempt
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.dashboard'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template('login.jinja2.html',
                           form=form,
                           title='Log in.',
                           template='login-page',
                           body="Log in with your User account.")

@auth_bp.route('/c_signup', methods=['GET', 'POST'])
def c_signup():
    """
    Sign-up form to create new user accounts.
    GET: Serve sign-up page.
    POST: Validate form, create account, redirect user to dashboard.
    """
    form = CustomerSignupForm()
    if form.is_submitted():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            customer = Customer(name=form.name.data,
                        email=form.email.data,
                        )
            customer.set_password(form.password.data)
            db.session.add(customer)
            db.session.commit()  # Create new user
            # rec = [form.email.data]
            # msg =Message("Registration",
            #              sender=("GoGlean","iyerarchith@gmail.com"),
            #              recipients=rec,
            #              body='<h3>Thanks for registering with GoGlean!</h3>'
            #              )
            # Thread(target=send_email, args=(app, msg)).start()
            return redirect(url_for('main_bp.cover'))
        flash('A user already exists with that email address.')
    return render_template('c_signup.jinja2.html',
                           title='Create an Account.',
                           form=form,
                           template='signup-page',
                           body="Sign up for a user account.")

@auth_bp.route('/c_login', methods=['GET', 'POST'])
def c_login():
    """
    Log-in page for registered users.
    GET: Serve Log-in page.
    POST: Validate form and redirect user to dashboard.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.cover'))  # Bypass if user is logged in

    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()  # Validate Login Attempt
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.cover'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.c_login'))
    return render_template('c_login.jinja2.html',
                           form=form,
                           title='Log in.',
                           template='login-page',
                           body="Log in with your User account.")


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))
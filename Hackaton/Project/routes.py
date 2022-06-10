from flask import Blueprint, render_template, redirect, url_for,session
from flask_login import current_user, login_required, logout_user
import time
from . models import send_email,get_reset_token , verify_reset_token,verify_reset_token_customer,c_send_email
from .models import User
from time import time
from . import db,mail
from Project.forms import EventForm,UpdateForm,FarmSearchForm
from .models import Event
from datetime import datetime
from flask_mail import Message
from flask import request,flash
from . import getDistance
from geopy.geocoders import Nominatim
from werkzeug.utils import secure_filename
import os
from . models import User , Customer
from PIL import Image
from flask_jwt_extended import jwt_required,create_access_token

dirt = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = dirt + "/static/Uploads/"
OPEN_IMAGE = dirt + "/static/Uploads/"
ALLOWED_EXTENSIONS = {'JPG', 'jpg'}
# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


def verify_email(email):
    user = User.query.filter_by(email=email).first()
    return user

def verify_Customer_email(email):
    c_user = Customer.query.filter_by(email=email).first()
    return c_user



@main_bp.route('/password_reset', methods=['POST',"GET"])
def reset():
    if request.method == 'GET':
        return render_template('reset.html')
    if request.method == "POST":
        email = request.form.get('Email')
        user = verify_email(email)

        if user:
            send_email(user)
        return redirect(url_for('auth_bp.login'))

@main_bp.route("/C_password_reset", methods=["POST","GET"])
def c_reset():
    if request.method=='GET':
        return render_template('c_reset.html')
    if request.method == 'POST':
        email = request.form.get("Email")
        c_user = verify_Customer_email(email)

        if c_user:
            c_send_email(c_user)
        return redirect(url_for('auth_bp.c_login'))


@main_bp.route('/password_reset_verified/<token>', methods=['GET','POST'])
def reset_verified(token):
        user= verify_reset_token(token)
        if not user:
            print("no user found")
            return redirect(url_for('auth_bp.login'))
        password=request.form.get('password')
        if password:
            User.set_password(user,password)
            db.session.commit()
            return redirect(url_for('auth_bp.login'))
        return render_template('reset_verified.html')


@main_bp.route('/c_password_reset_verified/<token>', methods=['GET','POST'])
def c_reset_verified(token):
    c_user = verify_reset_token_customer(token)
    if not c_user:
        print("no user found")
        return redirect(url_for('auth_bp.c_login'))
    password = request.form.get('password')
    if password:
        Customer.set_password(c_user,password)
        db.session.commit()
        return redirect(url_for("auth_bp.c_login"))
    return render_template('c_reset_verified.html')



@main_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    result =Event.query.filter_by(email=current_user.email).first()
    if result is None:
        event = 'Click on Create Event to Create Your First Event'
        return render_template('dashboard.jinja2.html', current_user=current_user, event=event)
    else:
        event = 'Click on Create Event to View Your Event'
        return render_template('dashboard.jinja2.html', current_user=current_user, event=event,result=result)


@main_bp.route('/', methods=['GET'])
def cover():
    """Logged-in User Dashboard."""
    return render_template('cover.html')


@main_bp.route("/customer_logout")
@login_required
def cumtomer_logout():
    logout_user()
    flash("You log out")
    return redirect(url_for('main_bp.cover'))


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    flash('You log out')
    return redirect(url_for('auth_bp.login'))

@main_bp.route("/create_event",methods=['GET', 'POST'])
@login_required
def create_event():
    if Event.query.filter_by(email=current_user.email).first() is None:
        form = EventForm()

        if form.is_submitted():
            # print(request.form['date'])
            # try:
                event = Event(
                        date = form.date.data,
                        email=current_user.email,
                        time=request.form['time'],
                        cap=request.form['cap'],
                        signedUp=0,
                        pricePerPound=request.form['pricePerPound'],
                        location=current_user.location,
                        address=current_user.address,
                        farmName = current_user.farmName,
                        farmType = current_user.farmType
                             )

                #Ignore this segment starting here
                # file = request.files['uploadimage']
                # filename = secure_filename(file.filename)
                # if filename.split('.')[1] not in ALLOWED_EXTENSIONS:
                #     flash("Our website does not support that type of extension")
                #
                # file.save(os.path.join(UPLOAD_FOLDER, str(current_user.email)) + '.jpg')
                # basewidth = 100
                # img = Image.open(OPEN_IMAGE + str(current_user.email) + '.jpg')
                # wpercent = (basewidth / float(img.size[0]))
                # hsize = int((float(img.size[1]) * float(wpercent)))
                # img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                # img.save(UPLOAD_FOLDER + str(current_user.email) + '.jpg')
                #Ending here, it saves the image of the farm uploaded by the farmer when creating an event to the image uploads folder, this is to verify that the Farmer is not lying about the event
                # try:
                db.session.add(event)
                db.session.commit()
            # except:
            #     flash("You have done error during filling the form")
            #     db.session.rollback()
            # except Exception as e:
            #     flash(e)
            #     db.session.rollback()

                return redirect(url_for('main_bp.cover'))
        return render_template('EventPage2.jinja2.html',form=form)
    else:
        form = UpdateForm()
        event = Event.query.filter_by(email=current_user.email).first()
        if form.validate_on_submit():
            Event.query.filter_by(email=current_user.email).first()
            db.session.query(Event).filter(Event.email == current_user.email).update({Event.signedUp: form.signedUp.data}, synchronize_session=False)
            try:
                db.session.commit()
            except:
                session.rollback()
            return redirect(url_for('main_bp.cover'))
        return render_template('dashboardIfCreatedEvent.jinja2.html',date=event.date,event_time=event.time,event_cap=event.cap,email=current_user.email,price=event.pricePerPound,form=form)


@main_bp.route("/search_event",methods=['GET', 'POST'])
def search_event():
    d = datetime.now()
    date = d.date()
    Event.query.filter_by(date=date).delete()
    try:
        db.session.commit()
    except:
       db.session.rollbacK()
    form = FarmSearchForm()
    results = []
    print(results)
    if current_user is None:
        status = 'You are not logged in'
    else:
        status = "You are logged in as Archith Iyer"
    if form.is_submitted():
        try:
            zipcode = form.zipCode.data
            state = form.state.data
            distance = form.select.data
            userLocation = str(state) + ' ' + str(zipcode)

            query = db.session.query(Event)

            geolocator = Nominatim(user_agent="zetauno1")
            userloc = geolocator.geocode(userLocation)
            lat2 = userloc.latitude
            long2 = userloc.longitude
            for i in query:
                loc = geolocator.geocode(i.location)
                lat1 = loc.latitude
                long1 = loc.longitude
                if getDistance.distance(lat1, lat2, long1, long2) < int(distance):
                    results.clear()
                    results.append(i)
            return render_template('searchEvent.jinja2.html', form=form, results=results)
        except AttributeError:
            return render_template('searchEvent.jinja2.html', form=form, results=results)
    return render_template('searchEvent.jinja2.html', form=form, results=results, status=status)

@main_bp.route('/About')
def about():
    return render_template('about.html')

@main_bp.route("/Contact")
def contact():
    return render_template("contact.html")











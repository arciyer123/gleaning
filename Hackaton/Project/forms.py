from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, IntegerField, DecimalField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from flask_wtf.file import FileField,FileAllowed
import os


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    name = StringField('Name',
                       validators=[DataRequired()])

    email = StringField('Email',
                        validators=[Length(min=6),
                                    Email(message='Enter a valid email.'),
                                    DataRequired()])
    address = StringField('Address',
                          validators=[DataRequired()])


    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])

    farmName = StringField('Farm Name',
                              validators=[Length(min=1, message='Enter the name of your farm')])

    farmType = StringField('Farm Type',
                              validators=[Length(min=1, message='Enter the type of produce your farm specializes in')])

    zip = IntegerField('Please enter your zip code')

    file = FileField('Please Provide an Agriculture Property Statement as Proof of Ownership',validators=[FileAllowed(['jpg','png','pdf'])])

    submit = SubmitField('Register')

class CustomerSignupForm(FlaskForm):
    """User Sign-up Form."""
    name = StringField('Name',
                       validators=[DataRequired()])

    email = StringField('Email',
                        validators=[Length(min=6),
                                    Email(message='Enter a valid email.'),
                                    DataRequired()])
    address = StringField('Address of Farm',
                        validators=[Length(min=11, message='Enter a valid phone number')])


    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])

    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField('Email', validators=[DataRequired(),
                                             Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class CustomerLoginForm(FlaskForm):
        """User Log-in Form."""
        email = StringField('Email', validators=[DataRequired(),
                                                 Email(message='Enter a valid email.')])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Log In')

class EventForm(FlaskForm):

    uploadimage = FileField(validators=[])

    date = DateField('Event Date', format='%m/%d/%Y',validators=[DataRequired()])

    time = SelectField('Please enter the time of the event', choices=[('10:00AM', '10:00AM'), ('11:00AM', '11:00AM'), ('12:00PM', '12:00PM'),('1:00PM', '1:00PM'),('2:00PM', '2:00PM'),('3:00PM', '3:00PM'),('4:00PM', '4:00PM'),('5:00PM', '5:00PM'),('6:00PM', '6:00PM')],validators=[DataRequired()])

    cap = StringField('Please Choose the max Number of People at your event')

    signedUp = StringField('Everytime you recieve an event signup email, update this count')

    pricePerPound = StringField('Please enter the price per pound of your produce',validators=[DataRequired()])

    submit = SubmitField('Create Event')

class UpdateForm(FlaskForm):
    signedUp = StringField('Everytime you recieve an event signup email, update this count')

    submit = SubmitField('Update Event')

class FarmSearchForm(FlaskForm):
    states = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
              "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
              "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
              "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
              "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
              "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
              "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
              "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
              "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
              "WI": "Wisconsin", "WY": "Wyoming"}
    list = [(v, k) for k, v in states.items()]

    state = SelectField("Please Enter the name of your State",choices=list)

    zipCode = StringField("Please Enter Your Zip Code",validators=[DataRequired()])

    distanceToFarm = [(50, 50),
               (100, 100),
               (200, 200)]

    select = SelectField('Search Radius',choices=distanceToFarm)

    search = StringField('Produce You Are Interested In',validators=[DataRequired()])

    submit = SubmitField('Find Events')




from flask_wtf import FlaskForm
from flask_behind_proxy import FlaskBehindProxy
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

# registration form for new users 
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# After registering, user can log in with this form
class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')

# Form for users to input valid coordinates on the coordinate page
class CoordinateForm(FlaskForm):
    start_lat = FloatField('Start Latitude', validators=[DataRequired(message="Start Latitude is required."),
        NumberRange(min=-90, max=90, message="Latitude must be between -90 and 90.")])
    
    start_long = FloatField('Start Longitude', validators=[ DataRequired(message="Start Longitude is required."),
        NumberRange(min=-180, max=180, message="Longitude must be between -180 and 180.")])
    
    end_lat = FloatField('End Latitude', validators=[DataRequired(message="End Latitude is required."),
        NumberRange(min=-90, max=90, message="Latitude must be between -90 and 90.")
    ])
    
    end_long = FloatField('End Longitude', validators=[DataRequired(message="End Longitude is required."),
        NumberRange(min=-180, max=180, message="Longitude must be between -180 and 180.")])

    trip_name = StringField('Trip Name', validators=[DataRequired(message="Please enter a trip name!")])
    submit = SubmitField('Save Trip')

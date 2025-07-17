import os
from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import RegistrationForm, LoginForm
import sqlalchemy as db
import sys
from sqlalchemy import Table, Column, FLOAT, String, MetaData, insert, update
import os

from database import db as user_db
from trips_database import TripsDatabase 

trips_db = TripsDatabase()

sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from geoapify import get_route, get_coordinates

# include api directory for geoapify
sys.path.insert(0, 'week-3-project/api')

app = Flask(__name__) 
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  

@app.route("/")                       
def home_page():
    return render_template('index.html') 

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # validators for username and email uniqueness
        if user_db.username_exists(username):
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('registration.html', title='Register', form=form)
        
        if user_db.email_exists(email):
            flash('Email already used. Please use a different email.', 'danger')
            return render_template('registration.html', title='Register', form=form)
        
        try:
            # create new user
            user_id = user_db.create_user(username, email, password)
            flash(f'Account created for {username}!', 'success')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('registration.html', title='Register', form=form)
    return render_template('registration.html', title='Register', form=form)



@app.route("/map", methods=["GET", "POST"])
def map():
    if request.method == "POST":
        start_lat = request.form["start_lat"]
        start_long = request.form["start_long"]
        end_lat = request.form["end_lat"]
        end_long = request.form["end_long"]
        trip_name = request.form.get("trip_name", "Untitled Trip")
        user_id = session.get("user_id")

        # save trip to database
        trips_db.save_trip(
            user_id=user_id,
            trip_name=trip_name,
            start_lat=start_lat,
            start_lon=start_long,
            end_lat=end_lat,
            end_lon=end_long
        )

        # get route data and render map
        route = get_route(start_lat, start_long, end_lat, end_long)
        coords = get_coordinates(route)
        return render_template("map.html", coords=coords)
    
    # Calculate center of polyline for improved display
    # center_lat = (start_lat+end_lat)/2
    # center_long = (start_long+end_long)/2

    return render_template("map.html")
  
    

'''@app.route("/register")
def register():
    return render_template('registration.html')'''

@app.route("/coordinates")
def coordinates():
    return render_template('coordinates.html')

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # authenticate user
        user = user_db.authenticate_user(username, password)
        
        if user:
            # store user info in session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['logged_in'] = True
            
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('coordinates'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', title='Login', form=form)

    
if __name__ == '__main__':        
    #db_init()      
    app.run(debug=True, host="0.0.0.0", port=5001)
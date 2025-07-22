import os
from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import RegistrationForm, LoginForm, CoordinateForm
import sqlalchemy as db
import sys
from sqlalchemy import Table, Column, FLOAT, String, MetaData, insert, update
import os

from database import db as user_db
from trips_database import TripsDatabase 

trips_db = TripsDatabase()

sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from geoapify import get_route, get_coordinates, get_properties, get_fuel_stations_along_route, get_fuel_coordinates, get_fuel_addresses
from tollguru import get_trip_cost

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
    form = CoordinateForm()
    user_id = session.get("user_id")
    trips = trips_db.get_user_trips(user_id)

    
    if request.method == "POST" and form.validate_on_submit():
        '''start_lat = request.form["start_lat"]
        start_long = request.form["start_long"]
        end_lat = request.form["end_lat"]
        end_long = request.form["end_long"]
        trip_name = request.form.get("trip_name", "Untitled Trip")'''

        start_lat = form.start_lat.data
        start_long = form.start_long.data
        end_lat = form.end_lat.data
        end_long = form.end_long.data
        trip_name = form.trip_name.data.strip() or "Untitled Trip"
        

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
        
        # if not route:
        #     flash("Could not fetch route from API.", "danger")
        #     return redirect(url_for("home_page"))
        
        coords = get_coordinates(route)
        props = get_properties(route)

        toll_guru_coords = [coord[::-1] for coord in coords] #revers lon lat for tollguru
        trip_cost = get_trip_cost(toll_guru_coords,props)
        
        # get gas station coords
        lonlat = [[cord[1], cord[0]] for cord in coords]
        stations = get_fuel_stations_along_route(lonlat)
        station_cords = get_fuel_coordinates(stations)
        print(station_cords)
        
        # get gas station brand and address
        # Test coordinates
        # 32.777415514467855 -96.78841389107889
        # 30.259838489967215 -97.74602960670074
        
        # get gas station brands and addresses
        station_info = get_fuel_addresses(stations) or []

        return render_template("map.html", coords=coords, trip_cost=trip_cost, gas_cords=station_cords, station_info=station_info)
    
    return render_template('coordinates.html', form=form, trips=trips)
    

'''@app.route("/register")
def register():
    return render_template('registration.html')'''

@app.route("/coordinates")
def coordinates():
    form = CoordinateForm()
    user_id = session["user_id"]
    trips = trips_db.get_user_trips(user_id)
    return render_template("coordinates.html", trips=trips, form=form)

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
from flask import Flask, render_template, flash, redirect, url_for, request
import sqlalchemy as db
import sys
from sqlalchemy import Table, Column, FLOAT, String, MetaData, insert, update
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from geoapify import get_route, get_coordinates

# include api directory for geoapify
sys.path.insert(0, 'week-3-project/api')

# Sets up database with columns for starting/end coordinates and estimated total price
def db_init():
    engine = db.create_engine('sqlite:///trips_database.db')
    metadata = MetaData()
    
    trips_table = Table('trips', metadata,
                        Column('start', String),
                        Column('end', String),
                        Column('costs', FLOAT),
                        db.PrimaryKeyConstraint('start', 'end'))
    
    metadata.create_all(engine)
    with engine.connect() as connection:
        stmt = insert(trips_table).values(start=0,
                                        end=2,
                                        costs=2)
        connection.execute(stmt)
        
        res = connection.execute(db.text("SELECT * FROM trips"))
        for rows in res:
            print(rows)
    
    return engine, trips_table

def insert_db():
    engine, trips_table = db_init()
    
    
app = Flask(__name__)                    
@app.route("/")                       
def home_page():
    return render_template('index.html') 

'''@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) 
    return render_template('register.html', title='Register', form=form)'''

@app.route("/map", methods=["GET", "POST"])
def map():
    start_lat = request.form["start_lat"]
    start_long = request.form["start_long"]
    end_lat = request.form["end_lat"]
    end_long = request.form["end_long"]
    
    # Calculate center of polyline for improved display
    # center_lat = (start_lat+end_lat)/2
    # center_long = (start_long+end_long)/2
    
    route = get_route(start_lat, start_long, end_lat, end_long)         # Get route data in JSON format
    coords = get_coordinates(route)
    
    
    return render_template("map.html", coords=coords)

@app.route("/register")
def register():
    return render_template('registration.html')

@app.route("/coordinates")
def coordinates():
    return render_template('coordinates.html')
    
if __name__ == '__main__':        
    db_init()      
    app.run(debug=True, host="0.0.0.0", port=5001)
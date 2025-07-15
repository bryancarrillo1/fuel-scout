from flask import Flask
import sqlalchemy as db
from sqlalchemy import Table, Column, FLOAT, String, MetaData, insert, update

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

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) 
    return render_template('register.html', title='Register', form=form)

    
if __name__ == '__main__':        
    db_init()      
    app.run(debug=True, host="0.0.0.0")
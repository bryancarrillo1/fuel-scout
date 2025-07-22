import sqlite3
from datetime import datetime
from contextlib import contextmanager

class TripsDatabase:
    def __init__(self, db_path='trips.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    trip_name TEXT,
                    start_lat TEXT NOT NULL,
                    start_lon TEXT NOT NULL,
                    end_lat TEXT,
                    end_lon TEXT
                )
            ''')
            
            conn.commit()
    
    @contextmanager
    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def save_trip(self, user_id, trip_name, start_lat, start_lon, end_lat, end_lon):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO trips (user_id, trip_name, start_lat, start_lon, 
                                 end_lat, end_lon)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, trip_name, start_lat, start_lon, 
                  end_lat, end_lon))
            conn.commit()
            return cursor.lastrowid
    
    def get_user_trips(self, user_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM trips 
                WHERE user_id = ? 
            ''', (user_id,))
            return cursor.fetchall()
    
    def get_trip_by_id(self, trip_id, user_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM trips 
                WHERE id = ? AND user_id = ?
            ''', (trip_id, user_id))
            return cursor.fetchone()
    
# Initialize trips database
trips_db = TripsDatabase()
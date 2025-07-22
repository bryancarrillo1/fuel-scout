import sqlite3
from datetime import datetime
from contextlib import contextmanager

class Database:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        #initialize database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
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
    
    def create_user(self, username, email, password):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (username, email, password)
                    VALUES (?, ?, ?)
                ''', (username, email, password))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError as e:
                if 'username' in str(e):
                    raise ValueError("Username already exists")
                elif 'email' in str(e):
                    raise ValueError("Email already exists")
                else:
                    raise ValueError("User creation failed")
    
    def get_user_by_username(self, username):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            return cursor.fetchone()
    
    def get_user_by_email(self, email):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            return cursor.fetchone()
    
    def authenticate_user(self, username, password):
        # checks if user is in database for login purposes
        user = self.get_user_by_username(username)
        if user and user['password'] == password:
            return user
        return None
    
    def username_exists(self, username):
        return self.get_user_by_username(username) is not None
    
    def email_exists(self, email):
        return self.get_user_by_email(email) is not None
    
db = Database()
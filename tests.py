import unittest
from app import app, trips_db

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
    def test_home(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_map(self):
        response = self.app.get('map', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_coordinates(self):
        with self.app.session_transaction() as session:
            session['user_id'] = 1
        response = self.app.get('/coordinates', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_login(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_register(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_data_base(self):
        test_id = 1
        dummy_trip = {
            'user_id': test_id,
            'trip_name': 'Test Trip',
            'start_lat': 12.34,
            'start_long': 56.78,
            'end_lat': 90.12,
            'end_long': 34.56
        }
        trips_db.save_trip('Untitled Trip', 10.0, 20.0, 30.0, 40.0, 10.0)
        trips = trips_db.get_user_trips(test_id)
        trip_names = [trip['trip_name'] for trip in trips]
        self.assertIn("Untitled Trip", trip_names)
    
        

if __name__ == "__main__":
    unittest.main()


import unittest
from app import app

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
    
    def test_home(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_map(self):
        response = self.app.get('map', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        

if __name__ == "__main__":
    unittest.main()


import unittest
import projectWeb

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = projectWeb.app.test_client()

    def tearDown(self):
        pass

    def test_home_page(self):
        rv = self.app.get('/')
        assert b'Freddie Lochner' in rv.data

    def test_link_to_my_page(self):
        rv = self.app.get('/')  
        assert b'Speed Racer' in rv.data 

    def test_my_topic(self):
        rv = self.app.get('/SpeedRacer')  
        assert b'Speed Racer' in rv.data 

if __name__ == '__main__':
    unittest.main()
    
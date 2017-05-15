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

    def test_Speed_page(self):
        rv = self.app.get('/SpeedRacer')
        assert b'Speed Racer' in rv.data

    def test_Archer_page(self):
        rv = self.app.get('/Archer')
        assert b'Archer' in rv.data

if __name__ == '__main__':
    unittest.main()
    
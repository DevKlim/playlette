import unittest
from app import app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_predict(self):
        response = self.app.post('/predict', json={'features': [0.5, 0.8, 0.6]})
        self.assertEqual(response.status_code, 200)
        self.assertIn('color', response.get_json())

if __name__ == '__main__':
    unittest.main()

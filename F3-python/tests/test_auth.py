import unittest
import json
from app import app

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_ping(self):
        response = self.app.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'ok': True})

    def test_auth_success(self):
        response = self.app.post('/authenticate',
                                 data=json.dumps({'user': 'test', 'password': 'test'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('auth_token', response.json)

    def test_auth_failure(self):
        response = self.app.post('/authenticate',
                                 data=json.dumps({'user': 'wrong', 'password': 'wrong'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('errors', response.json)

    def test_auth_missing_fields(self):
        response = self.app.post('/authenticate',
                                 data=json.dumps({'user': 'test'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json)

if __name__ == '__main__':
    unittest.main()

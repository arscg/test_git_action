# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 19:30:39 2024

@author: arsca
"""

import unittest
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()

        hashed_password = generate_password_hash('password', method='sha256')
        user = User(username='testuser', password=hashed_password)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

if __name__ == '__main__':
    unittest.main()

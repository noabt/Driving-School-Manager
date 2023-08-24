import unittest
from flask import Flask, jsonify
from unittest.mock import patch
from website import app, db, User  

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use an in-memory SQLite database for testing
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        new_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        with patch.object(User, 'create') as mock_create:
            mock_create.return_value = User(**new_user_data)

            response = self.app.post('/sign-up', json=new_user_data)

            self.assertEqual(response.status_code, 201)  
            self.assertTrue('user_id' in response.json) 

if __name__ == '__main__':
    unittest.main()

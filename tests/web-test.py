import unittest
from flask import url_for
from flask_testing import TestCase
from website import app, db, User  

class TestFlaskApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use an in-memory SQLite database for testing
        return app

    def setUp(self):
        db.create_all()
        user = User(username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_authenticated_homepage(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('home.html')  

if __name__ == '__main__':
    unittest.main()

import unittest
from flask import Flask
from flask_testing import TestCase

class TestFlaskApp(TestCase):
    
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        @app.route('/')
        def index():
            return 'Hello, World!'
        
        return app
    
    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Hello, World!')

if __name__ == '__main__':
    unittest.main()






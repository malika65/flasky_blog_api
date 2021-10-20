import unittest
from flask import current_app

from app import create_app, db

class BasicsTestCase(unittest.TestCase):
    
    # run before and after each test
    # Create an environment for the test that is close to that of
    # a running application
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # run before and after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    # executed as tests
    def test_app_exists(self):
        self.assertFalse(current_app is None)
    
    # executed as tests
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
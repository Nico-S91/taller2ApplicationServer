# from flask.ext import restful
import unittest
import os
import json
import sys
from main_app import application

class TestEnpoints(unittest.TestCase):

    def setUp(self):
        ''' fire up a test instance of the flask app '''
        self.app = application.test_client()
        self.app.testing = True
        # self.api = app.app.api
        self.test_brand_name = 'Llevame'

    def test_get(self):
        result = self.app.get('/todo/api/v1.0/tasks', headers=[('user-api-key','<redacted>')])
        print(result.data)
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
import unittest
import json
import sys, os


from context import car_service
from context import dbhandler

# from car_serivce import app
# from nose.tools import *

class CarServiceTestCase(unittest.TestCase):
    """This class represents the car_serivce test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = car_service.create_app(config_name="testing")
        self.client = self.app.test_client

        with self.app.app_context():
            # create all tables
            car_service.db.session.close()
            car_service.db.drop_all()
            car_service.db.create_all()     
        
        self.access_token = "someToken"

    
    def test_all_cars(self):
        """Test API can create a bucketlist (POST request)"""
        

        res = self.client().get(
            '/cars',
            headers=dict(Authorization="Bearer " + self.access_token))

        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', str(data.get('status')))
        self.assertEqual([], data.get('data'))


    def test_specific_cars(self):
        """Test API can create a bucketlist (POST request)"""

        # dbhandler.intialize_db(car_service.db,car_service.app)


        res = self.client().get(
            '/car/somerandomid',
            headers=dict(Authorization="Bearer " + self.access_token))

        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        # print(data)
        self.assertIn('failure', str(data.get('status')))
        self.assertIn('Not Found', str(data.get('error')))



    def test_avg_price(self):
        """Test API can create a bucketlist (POST request)"""

        # dbhandler.intialize_db(car_service.db,car_service.app)

        

        res = self.client().get(
            '/car/aggregator/price',
            headers=dict(Authorization="Bearer " + self.access_token))

        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', str(data.get('status')))
        self.assertEqual(None, data.get('data'))



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
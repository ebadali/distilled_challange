import unittest
import json
import sys, os, csv


from context import car_service
from context import dbhandler

class CarServiceTestForFailedInstances(unittest.TestCase):
    """This class represents the car_serivce unsuccessfull test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = car_service.create_app(config_name="testing")
        self.client = self.app.test_client

        # Emptying the database to test against the empty tables
        with self.app.app_context():
            # create all tables
            print('emptying all the db')
            # car_service.db.session.close()
            car_service.db.drop_all()
            car_service.db.create_all()     
        
        self.access_token = "Some_Predefined_Token"

    
    def test_all_cars(self):
        """Tests API to fetch all cars unsuccessfully without a crash (GET request)"""
        

        res = self.client().get(
            '/cars',
            headers=dict(Authorization="Bearer " + self.access_token))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', str(data.get('status')))
        self.assertEqual([], data.get('data'))


    def test_specific_cars(self):
        """Tests API to fetch a non existing car (GET request)"""

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
        """Tests API to fetch the average prices on non existing resources (GET request)"""

        # dbhandler.intialize_db(car_service.db,car_service.app)

        

        res = self.client().get(
            '/car/aggregator/price',
            headers=dict(Authorization="Bearer " + self.access_token))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', str(data.get('status')))
        self.assertEqual(None, data.get('data'))

    def test_invalid_bearer(self):
        """Tests API to fetch some resource with invalid bearer. Stands true for all apis. (GET request)"""
        

        res = self.client().get(
            '/car/2',
            headers=dict(Authorization="Bearer " + "Some Invalid bearer"))

        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertIn('failure', str(data.get('status')))


class CarServiceTestForSuccessfullInstances(unittest.TestCase):
    """This class represents the car_serivce successfull test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = car_service.create_app(config_name="staging")
        self.client = self.app.test_client
        # an auth token for apis.        
        self.access_token = "Some_Predefined_Token"

    
    def test_get_all_cars(self):
        """Tests API to fetch all the cars  (GET request)"""
        

        res = self.client().get(
            '/cars',
            headers=dict(Authorization="Bearer " + self.access_token))

        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', str(data.get('status')))
        self.assertNotEqual([], data.get('data'))


    def test_get_specific_car(self):
        """Tests API to fetch a specific car (GET request)"""

        # dbhandler.intialize_db(car_service.db,car_service.app)


        res = self.client().get(
            '/car/1',
            headers=dict(Authorization="Bearer " + self.access_token))

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        
        self.assertIn('success', str(data.get('status')))
        self.assertEqual(dict, type(data.get('data')))


    def test_get_avg_price_api(self):
        """Tests API to test the successfull base scenario  (GET request)"""

        # dbhandler.intialize_db(car_service.db,car_service.app)
        res = self.client().get(
            '/car/aggregator/price',
            headers=dict(Authorization="Bearer " + self.access_token))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', str(data.get('status')))
        self.assertEqual(float, type(data.get('data')))


    def test_get_avg_price_api_query(self):
        """Tests API for query params (GET request)"""

        # dbhandler.intialize_db(car_service.db,car_service.app)
        res = self.client().get(
            '/car/aggregator/price?make=Nissan',
            headers=dict(Authorization="Bearer " + self.access_token))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', str(data.get('status')))
        self.assertEqual(float, type(data.get('data')))


        

    def test_get_avg_price_value(self):
        """Tests API for actual average price value (GET request)"""
        
        # Reading data from the csv file and calculating the average of
        # certain car make 'Nissas'.

        csv.register_dialect('myDialect',delimiter = ',',quoting=csv.QUOTE_ALL,skipinitialspace=True)
        nissan_avg = 0  
        with open('car_data.csv', 'r') as f:
            reader = csv.reader(f, dialect='myDialect')
            next(reader, None)

            nissans_prices = [ float(row[6]) for row in reader if 'Nissan' in row[0] ]
            nissan_avg = sum(nissans_prices) / float(len(nissans_prices))

        res = self.client().get(
            '/car/aggregator/price?make=Nissan',
            headers=dict(Authorization="Bearer " + self.access_token))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', str(data.get('status')))
        self.assertEqual(nissan_avg, float(data.get('data')))



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
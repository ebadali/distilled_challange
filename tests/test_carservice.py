import unittest
import os
import json
import config
from car_serivce import app


class CarServiceTestCase(unittest.TestCase):
    """This class represents the car_serivce test case"""

    # def setUp(self):
    #     """Define test variables and initialize app."""
    #     self.app = create_app(config_name="testing")
    #     self.client = self.app.test_client
    #     self.bucketlist = {'name': 'Go to Borabora for vacay'}

    #     # binds the app to the current context
    #     with self.app.app_context():
    #         # create all tables
    #         db.session.close()
    #         db.drop_all()
    #         db.create_all()


    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = "asdsa"

        res = self.client().post(
            '/cars/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('success', str(res.data['status']))

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
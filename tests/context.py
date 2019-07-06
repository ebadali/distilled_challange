import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# print('--')
print(sys.path)
import car_service
from car_service.datastore import dbhandler
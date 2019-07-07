import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# This will enable me to add more tests scripts without worrying about individual imports.
import car_service
from car_service.datastore import dbhandler
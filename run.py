#! /usr/local/bin/python3
import os
from car_service import create_app

config_name = os.getenv('APP_SETTINGS','staging')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#! /usr/local/bin/python3
import os
from car_service import create_app

# app.run(host='0.0.0.0', port=80, debug=True)



# from app import create_app

config_name = os.getenv('APP_SETTINGS','testing')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()

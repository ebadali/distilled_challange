# from flask import Flask, g
# from flask import current_app as app

# from car_service import app
# # app = Flask('car_service')
# print ("flask app name 2")
# print (app)
# print (Flask.app_context)
# # app = Flask.app_context
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test2.db'
# # Use built in SQLAlchemy's built-in event system instead of
# # Flask's SQLAlchemy event system
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)


# # Circualr dependency. It is fine !
# from datastore.models import Car

import os,sys
import markdown
from functools import wraps

import logging
from logging.handlers import RotatingFileHandler
# Import the framework
from flask import Flask, g, request, abort
from flask_restful import Resource, reqparse
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy

from config import app_config
from car_service.utils import responces


# Create an instance of Flask
# app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test3.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'people.db')

# # Use built in SQLAlchemy's built-in event system instead of
# # Flask's SQLAlchemy event system
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# Circular reference

# Swagger stuffs
### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)

### end swagger specific ###

db = SQLAlchemy()
app = None


def create_app(config_name):

    from car_service.datastore import dbhandler
    from car_service.datastore.models import Car

    # app = FlaskAPI(__name__, instance_relative_config=True)
    # overriding Werkzeugs built-in password hashing utilities using Bcrypt.
    # bcrypt = Bcrypt(app)
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    db.init_app(app)

    
    handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=100000, backupCount=3)
    logger = logging.getLogger('tdm')
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)


    # enforcing the api check
    def require_api_key(api_method):
        @wraps(api_method)

        # enables a very basic api auth against a hardcoded secret key
        def check_api_key(*args, **kwargs):
            apikey = request.headers.get('Authorization')

            if apikey and len(apikey.split(" ")) == 2 and apikey.split(" ")[1] == app.config['API_ACCESS_TOKEN']:
                return api_method(*args, **kwargs)
            else:
                abort(401)
                return None

        return check_api_key

    @app.teardown_appcontext
    def teardown_db(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @app.before_first_request
    def create_tables():
        # db.create_all()
        if app.config['DEBUG'] == False:
            dbhandler.intialize_db(db,app)

    @app.before_request
    def log_request_info():
        logger.info('Headers: %s', request.headers)
        logger.debug('Body: %s', request.get_data())
        

    @app.route("/")
    def index():
        """Present some documentation"""

        # Open the README file
        with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

            # Read the content of the file
            content = markdown_file.read()

            # Convert to HTML
            return markdown.markdown(content)


    @app.route("/health")
    def health_check():
        """health check"""
        
        return responces.getSuccessResponse()

    @app.route("/cars", methods=['GET'])
    @require_api_key
    def get_all_cars():
        """get all cars"""
        # TOD: Add pagination or limit response to certain limit!
        all_cars = dbhandler.get_all_cars()

        return responces.getSuccessResponse(data=all_cars)


    @app.route("/car/<string:identifier>",methods=['GET'])
    @require_api_key
    def get_a_car(identifier):
        """get specific car without chases number"""

        single_car = dbhandler.get_specific_cars(identifier)
        if single_car:
            return responces.getSuccessResponse(data=single_car)

        return responces.getFailResponse(reason="Not Found")

    @app.route("/car/aggregator/price",methods=['GET'])
    @require_api_key
    def get_avg_price():
        """Gets the average price by make, model or year. Or combinition of both"""
        
        # Parsing the query string
        make = request.args.get('make',None)
        model = request.args.get('model',None)
        year = request.args.get('year',None)



        avg_price = dbhandler.get_avg_price(db,make_filter=make,model_filter=model,year_filter=year)
        if not avg_price:
            responces.getFailResponse(reason='empty database')
        return responces.getSuccessResponse(data=avg_price)


    @app.errorhandler(Exception)
    def unhandled_exception(e):

        msg = "Erorr: {} ".format(e)
        print(msg)
        # print(exc_type, fname, exc_tb.tb_lineno)
        # app.logger.error('Unhandled Exception: %s', (e))
        return responces.getFailResponse(msg)

    @app.errorhandler(401)
    def not_found_error(error):
        return responces.getFailResponse(reason='Unauthorized access',error=401)


    @app.errorhandler(404)
    def not_found_error(error):
        return responces.getFailResponse(reason='Not found',error=404)

    @app.errorhandler(500)
    def internal_error(error):
        return responces.getFailResponse(reason='Internal error',error=500)

    return app

# TODO: Logger settings.


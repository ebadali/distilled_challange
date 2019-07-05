#!/usr/local/bin/python3
import markdown
import os

# Import the framework
from flask import Flask, g, request
from flask_restful import Resource, reqparse
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy

# Create an instance of Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test3.db'
# Use built in SQLAlchemy's built-in event system instead of
# Flask's SQLAlchemy event system
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Circular reference
from car_service.utils import responces
from car_service.datastore import dbhandler


# Swagger stuffs
### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

### end swagger specific ###

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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
def get_all_cars():
    """get all cars"""
    # TOD: Add pagination or limit response to certain limit!
    all_cars = dbhandler.get_all_cars()
    return responces.getSuccessResponse(data=all_cars)


@app.route("/car/<string:identifier>",methods=['GET'])
def get_a_car(identifier):
    """get specific car without chases number"""

    single_car = dbhandler.get_specific_cars(identifier)
    if single_car:
        return responces.getSuccessResponse(data=single_car)

    return responces.getFailResponse(reason="Not Found")

# @autherize_check
# /car/aggregator/price?include=make,model,year
@app.route("/car/aggregator/price",methods=['GET'])
def get_avg_price():
    """Gets the average price by make, model or year. Or combinition of both"""
    
    # Parsing the query string
    included_query = request.args.get('include','')
    if included_query:
        pass

    avg_price = dbhandler.get_avg_price(db)
    return responces.getSuccessResponse(data=avg_price)


@app.errorhandler(Exception)
def unhandled_exception(e):

    msg = "Erorr: {} ".format(e)
    
    app.logger.error('Unhandled Exception: %s', (e))
    return responces.getFailResponse(msg)


# TODO: Logger settings.


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        description="Seans-Python-Flask-REST-Boilerplate")

    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = int(os.environ.get('PORT', 5000))
    dbhandler.intialize_db(db)
    if ARGS.debug:
        print("Running in debug mode")
        CORS = CORS(app)
        app.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        app.run(host='0.0.0.0', port=PORT, debug=False)

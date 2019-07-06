import os,sys
import markdown
from functools import wraps

# Import the framework
from flask import Flask, g, request
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

    dbhandler.intialize_db(db,app)

    # enforcing the api check
    def require_api_key(api_method):
        @wraps(api_method)

        def check_api_key(*args, **kwargs):
            apikey = request.headers.get('ApiKey')
            if apikey and apikey == SECRET_KEY:
                return api_method(*args, **kwargs)
            else:
                abort(401)

        return check_api_key

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

    # @require_api_key
    @app.route("/cars", methods=['GET'])
    def get_all_cars():
        """get all cars"""
        # TOD: Add pagination or limit response to certain limit!
        all_cars = dbhandler.get_all_cars()
        print('my car size '+ str(len(all_cars)))
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
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        app.logger.error('Unhandled Exception: %s', (e))
        return responces.getFailResponse(msg)


    @app.errorhandler(404)
    def not_found_error(error):
        return responces.getFailResponse(reason='Not found',error=404)

    @app.errorhandler(500)
    def internal_error(error):
        return responces.getFailResponse(reason='Internal error',error=500)

    return app

# TODO: Logger settings.


# if __name__ == '__main__':

#     PARSER = argparse.ArgumentParser(
#         description="Seans-Python-Flask-REST-Boilerplate")

#     PARSER.add_argument('--debug', action='store_true',
#                         help="Use flask debug/dev mode with file change reloading")
#     ARGS = PARSER.parse_args()

#     PORT = int(os.environ.get('PORT', 5000))
#     dbhandler.intialize_db(db)
#     if ARGS.debug:
#         print("Running in debug mode")
#         CORS = CORS(app)
#         app.run(host='0.0.0.0', port=PORT, debug=True)
#     else:
#         app.run(host='0.0.0.0', port=PORT, debug=False)

import csv
import shelve
from flask import Flask, g
from car_service.datastore.models import Car
from sqlalchemy import func

# from datastore import Car
# import Car
# from datastore.models import Car


def intialize_db(db,app):
    print ("reset db")
    with app.app_context():
        db.drop_all()
        db.create_all()

        res = Car.query.first()
        if not res:
            load_db(db)


def load_db(db):

    csv.register_dialect('myDialect',delimiter = ',',quoting=csv.QUOTE_ALL,skipinitialspace=True)

    with open('car_data.csv', 'r') as f:
        reader = csv.reader(f, dialect='myDialect')
        next(reader, None)

        for row in reader:
            db.session.add(
                Car(make=row[0], model=row[1], year=row[2], chassis_no=row[3], identifier=row[4], last_updated=row[5], price=row[6])
            )

        db.session.commit()



# reset_database()

def get_all_cars():

    all_cars = [ car.serialize for car in Car.query.all() ]

    return all_cars


def get_specific_cars(identifier):

    car_result = None
    try:
        car_result = Car.query.filter(Car.identifier == identifier).first()
    except Exception as e:        
        pass
        
    
    return car_result.serialize if car_result else None


def get_avg_price(db,make_filter=None,model_filter=None,year_filter=None):
    """Gets the average price by make, model or year. Or combinition of both"""
    # TODO: unscalable logic. Change that to catter more filters 

    data = None

    if make_filter and model_filter and year_filter:
        data = db.session.query(db.func.avg(Car.price)).filter(Car.make == make_filter, Car.model==model_filter,Car.year==year_filter).scalar()
    elif make_filter and model_filter:
        data = db.session.query(db.func.avg(Car.price)).filter(Car.make == make_filter, Car.year==model_filter).scalar()
    elif model_filter and year_filter: 
        data = db.session.query(db.func.avg(Car.price)).filter(Car.model == model_filter,Car.year==year_filter).scalar()
    elif year_filter and make_filter : 
        data = db.session.query(db.func.avg(Car.price)).filter(Car.make == make_filter,Car.year==year_filter).scalar()
    elif make_filter:
        data = db.session.query(db.func.avg(Car.price)).filter(Car.make == make_filter).scalar()
    elif model_filter:
        data = db.session.query(db.func.avg(Car.price)).filter(Car.model == model_filter).scalar()        
    elif year_filter:
        data = db.session.query(db.func.avg(Car.price)).filter(Car.year == year_filter).scalar()        
    else:
        data = db.session.query(db.func.avg(Car.price)).scalar()

  
    return data


import csv
import shelve
from flask import Flask, g
from car_service.datastore.models import Car, db
from sqlalchemy import func
from sqlalchemy.orm import load_only


############## Partial DDL ############## 
def intialize_db(app):
    ''' Initialized db, and load data from csv file if db is empty'''
    with app.app_context():
        db.drop_all()
        db.create_all()

        res = Car.query.first()
        if not res:
            load_db()


def load_db():
    '''load data from csv file into the database'''    
    csv.register_dialect('myDialect',delimiter = ',',quoting=csv.QUOTE_ALL,skipinitialspace=True)

    with open('car_data.csv', 'r') as f:
        reader = csv.reader(f, dialect='myDialect')
        next(reader, None)

        for row in reader:
            db.session.add(
                Car(make=row[0], model=row[1], year=row[2], chassis_no=row[3], identifier=row[4], last_updated=row[5], price=row[6])
            )

        db.session.commit()


############## DML ############## 
fields = ['make','model','year','identifier','last_updated', 'price']

def get_all_cars():
    """Gets all cars from the db. Returns empty array if db is empty"""

    # all_cars = [ car.serialize 
    #     for car in Car.query.all() ]
    all_cars = [ car.serialize for car in db.session.query(Car).options(load_only(*fields)).all() ]


    return all_cars


def get_specific_cars(identifier):
    """lookup and returns the specific car with identifier from the db. Returns None if not found"""

    car_result = None
    try:
        car_result = db.session.query(Car).options(load_only(*fields)).filter(Car.identifier == identifier).first()
        # car_result = Car.query.filter(Car.identifier == identifier).first()
    except Exception as e:        
        pass
        
    
    return car_result.serialize if car_result else None


def get_avg_price(make_filter=None,model_filter=None,year_filter=None):
    """Gets the average price by make, model or year. Or combinition of both. Returns the float value, None otherwise"""
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


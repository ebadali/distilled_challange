import csv
import shelve
from flask import Flask, g
from car_service.datastore.models import Car

# from datastore import Car
# import Car
# from datastore.models import Car


def intialize_db(db):
    print ("reset db")
    db.drop_all()
    db.create_all()

    res = Car.query.first()

    if not res:
        load_db(db)



def reset_database(db):
    print ("reset db")
    db.drop_all()
    db.create_all()
    res = Car.query.first()
    print (res)
    if not res:
        load_db(db)

def load_db(db):

    csv.register_dialect('myDialect',delimiter = ',',quoting=csv.QUOTE_ALL,skipinitialspace=True)

    with open('car_data.csv', 'r') as f:
        reader = csv.reader(f, dialect='myDialect')
        next(reader, None)
        i = 1
        for row in reader:
            db.session.add(
                Car(make=row[0], model=row[1], year=row[2], chassis_no=row[3], identifier=row[4], last_updated=row[5], price=row[6])
            )
            # i =+ 1
            # if i > 4:
            #     break
        db.session.commit()

def add_car(userObjec: Car):
    pass


# reset_database()

def get_all_cars():

    all_cars = [ car.serialize for car in Car.query.all() ]
    # print (all_cars)
    return all_cars


def get_specific_cars(identifier):

    car = Car.query.filter(Car.identifier == identifier).one()
    print (car)
    return car.serialize if car else None





# from datastore import db
from car_service import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


class Car(Base):
    __tablename__ = 'table_car'

    make = db.Column(db.String(80), unique=False, nullable=False)
    model = db.Column(db.String(120), unique=False, nullable=False)
    year = db.Column(db.String(80), unique=False, nullable=False)
    chassis_no = db.Column(db.String(120), unique=True, nullable=False)
    identifier = db.Column(db.Integer, unique=False)    
    last_updated = db.Column(db.String(80), unique=False)
    price = db.Column(db.String(120), unique=False)

    # New instance instantiation procedure
    def __init__(self, make, model, year,chassis_no,identifier,last_updated,price):

        self.make     = make
        self.model    = model
        self.year = year if year else ""
        self.chassis_no     = chassis_no
        self.identifier    = identifier
        self.last_updated = last_updated
        self.price = price if price else 0

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'make'         : self.make,
            'model'         : self.model,
            'year'         : self.year,
            'chassis_no'         : self.chassis_no,
            'identifier'         : self.identifier,
            # TODO: Handle the datetime. Lets keep it string for now
            'last_updated': self.last_updated,
            'price'         : self.price
   
        }

    def __repr__(self):
        return '<identifier %r>' % self.identifier


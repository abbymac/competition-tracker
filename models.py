from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


database_name = "capstone"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = "postgres://wiegupgmizfcym:555d35f3e5cd08525dc2109428d4f9ff0a60f37d21aa57e7b3a9926820b6d92b@ec2-54-156-73-147.compute-1.amazonaws.com:5432/d1vqqjqkf74gna"

app = Flask(__name__)
db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


racers = db.Table('racers', 
    db.Column('racer_id', db.Integer, db.ForeignKey('athletes.id'), primary_key=True),
    db.Column('race_id', db.Integer, db.ForeignKey('races.id'), primary_key=True)
)


class Venue(db.Model): 
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    # races = db.relationship('Race', backref='venues')
    
    def insert(self): 
        db.session.add(self)
        db.session.commit()
    
    def update(self): 
        db.session.commit()
    
    def delete(self): 
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address
        }

    def __repr__(self):
        return f'<Venue ID: {self.id}, name: {self.name}>'

class Athlete(db.Model): 
    __tablename__ = 'athletes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    division = db.Column(db.String(120), nullable=False)
    # races = db.relationship('Race', backref='athlete')

    def insert(self): 
        db.session.add(self)
        db.session.commit()
    
    def update(self): 
        db.session.commit()
    
    def delete(self): 
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'division': self.division
        }

    def __repr__(self):
        return f'<Athlete ID: {self.id}, name: {self.name}>'

class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    division = db.Column(db.String, nullable=False)
    prize = db.Column(db.Integer, nullable=False)
    athletes = db.relationship('Athlete', secondary=racers, 
        backref=db.backref('races', lazy=True))

    # athletes = db.relationship('Race', backref='athlete')
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_time': self.start_time,
            'division': self.division,
            'prize': self.prize,
            'venue_id': self.venue_id,
        }

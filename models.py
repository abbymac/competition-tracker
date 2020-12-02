from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


database_name = "capstone"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()



class Venue(db.Model): 
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    races = db.relationship('Race', backref='venues')

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
    races = db.relationship('Race', backref='athlete')

    def __repr__(self):
        return f'<Athlete ID: {self.id}, name: {self.name}>'

class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    division = db.Column(db.String, nullable=False)
    prize = db.Column(db.Integer, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('athletes.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)



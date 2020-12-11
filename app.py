import os
import sys
import json

from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pytz import utc
from flask_moment import Moment
from flask_migrate import Migrate
from datetime import datetime

from models import setup_db, db, Athlete, Venue, Race, racers

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)
  migrate = Migrate(app, db)
  

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.route('/')
  def index():
    print('success hit')
    return render_template('index.html')

  # ----------------------------------------------------------------------------------------
  # Athletes
  # ----------------------------------------------------------------------------------------

  @app.route('/api/athletes', methods=['GET'])
  def get_athletes(): 
    now = datetime.now(tz=None)
    print(now)
    athletes = Athlete.query.all()
    print(athletes)
    formatted_athletes = [athlete.format() for athlete in athletes]
    print(formatted_athletes)

    return jsonify({
      'success': True, 
      'athletes': formatted_athletes
    })

  @app.route('/api/athletes/<int:athlete_id>', methods=['PATCH'])
  def edit_athlete(athlete_id): 
    data = json.loads(request.data.decode('utf-8'))
    athlete = Athlete.query.filter(Athlete.id == athlete_id).one_or_none()
    
    name = data.get('name', None)
    age = data.get('age', None)
    city = data.get('city', None)
    state = data.get('state', None)
    phone = data.get('phone', None)
    division = data.get('division', None)

    if athlete is None: 
      return jsonify({
        'success': False, 
        'error': 404,
        'message': 'No such athlete found in database.'
      }), 404
    
    try: 
      if name:
        athlete.name = name 
      if age:
        athlete.age = age 
      if city:
        athlete.city = city 
      if state:
        athlete.state = state 
      if phone:
        athlete.phone = phone 
      if division:
        athlete.division = division

      athlete.update()
      return jsonify({
            'success': True
        }), 200

    except Exception as error_msg:
        print(error_msg)
        abort(422)
      
  @app.route('/api/athletes', methods=['POST'])
  def create_athlete(): 
    data = json.loads(request.data.decode('utf-8'))
    error = False

    name = data.get('name', None)
    age = data.get('age', None)
    city = data.get('city', None)
    state = data.get('state', None)
    phone = data.get('phone', None)
    division = data.get('division', None)

    try: 
      athlete = Athlete(
        name=name,
        age=age,
        city=city,
        state=state,
        phone=phone,
        division=division
      )
      athlete.insert()
      athlete.update()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info)
    finally: 
      db.session.close()
    if error: 
      abort(422)
      flash('An error occured. Athlete unsuccessfully created.')
    else: 
      return jsonify({
        'success': True,
        'message': 'Athlete created successfully'
      })

  @app.route('/api/athletes/<int:athlete_id>', methods=['DELETE'])
  def delete_athlete(athlete_id): 
    error = False 
    athlete = Athlete.query.filter(Athlete.id == athlete_id).one_or_none()

    if athlete is None: 
      return jsonify({
        'success': False, 
        'error': 404,
        'message': 'No such athlete found in database.'
      }), 404

    try: 
      athlete.delete()
    except: 
      db.session.rollback()
      error = True
    finally:
      db.session.close()
    if error:
      abort(500)
    else:
      return jsonify({
        'message': 'athlete deleted successfully',
        'success': True,
        'deleted': athlete_id
      })

  # ----------------------------------------------------------------------------------------
  # Venues
  # ----------------------------------------------------------------------------------------

  @app.route('/api/venues', methods=['GET'])
  def get_venues(): 
    venues = Venue.query.all()
    print(venues)
    formatted_venues = [venue.format() for venue in venues]
    print(formatted_venues)

    return jsonify({
      'success': True, 
      'venues': formatted_venues
    })

  @app.route('/api/venues', methods=['POST'])
  def create_venue(): 
    data = json.loads(request.data.decode('utf-8'))
    error = False 

    name = data.get('name', None)
    city = data.get('city', None)
    state = data.get('state', None)
    address = data.get('address', None)

    try: 
      venue = Venue(
        name = name, 
        city = city,
        state = state, 
        address = address
      )
      print(venue)
      venue.insert()
      venue.update()
    except: 
      error = True 
      db.session.rollback()
      print(sys.exc_info)
    finally: 
      db.session.close()
    if error: 
      abort(422)
    else: 
      return jsonify({
        'success': True, 
        'message': 'venue create successfully'
      })

  @app.route('/api/venues/<int:venue_id>', methods=['DELETE'])
  def delete_venue(venue_id): 
    error = False 
    try: 
      venue = Venue.query.get(venue_id)
      venue.delete()
    except: 
      db.session.rollback()
      error = True
    finally:
      db.session.close()
    if error:
      abort(500)
    else:
      return jsonify({
        'message': 'deleted successfully',
        'success': True,
        'deleted': venue_id
      })


  # ----------------------------------------------------------------------------------------
  # Races
  # ----------------------------------------------------------------------------------------

  @app.route('/api/races', methods=['GET'])
  def get_races(): 
    races = Race.query.all()

    def format(racer): 
      return  {
        'racer_id': racer.id,
        'name': racer.name,
        'city': racer.city, 
        'phone': racer.phone, 
        'state': racer.state, 
        'division': racer.division       
      }
    formatted_races = [race.format() for race in races]

    for comp in races: 
      rs = Athlete.query.join(racers).join(Race).filter((racers.c.racer_id == Athlete.id) & (racers.c.race_id == Race.id) & (racers.c.race_id == comp.id)).all()
    # print('t', rs)
    race_athletes = []
    for x in rs: 
      # print('x is', x)
      form = format(x)
      race_athletes.append(form)
      print('something', race_athletes)
    data = {}

    return jsonify({
      'success': True, 
      'races': formatted_races,
      'racer_athletes': race_athletes
    })

  @app.route('/api/races/<int:race_id>', methods=['GET'])
  def get_race_by_id(race_id):
    race = Race.query.filter(Race.id == race_id).one_or_none()
    if race is None:
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'No such race found in database.'
        }), 404
    
  # ----------------------------------------------------------------------------------------
  # Error Handlers
  # ----------------------------------------------------------------------------------------
  
  @app.errorhandler(400)
  def bad_request(error): 
      return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad request"
        }), 400

  @app.errorhandler(404)
  def not_found(error): 
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(422)
  def unproccesable(error): 
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable entity"
        }), 422

  @app.errorhandler(500)
  def unproccesable(error): 
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal Server Error"
        }), 500



  return app




APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
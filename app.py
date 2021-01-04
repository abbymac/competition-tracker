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
from auth import AuthError, requires_auth


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
    """ Get all athletes from DB

        Permissions: none required, read only

        Returns:
            - 200 status code with json obj of
              athletes in dict.
            - Example response:
            @TODO change to approp response.
                {
                    "drinks": [
                        {
                            "id": 1,
                            "recipe": [
                                {
                                    "color": "blue",
                                    "parts": 1
                                }
                            ],
                            "title": "Water"
                        }
                    ],
                    "success": true
                }

        Raises:
            - 404 if unable to find any corresponding athlete
    """
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
  @requires_auth('patch:information')
  def edit_athlete(payload, athlete_id):
    """ Edit an athlete in DB

        Permissions: patch:information

        Params: payload, athlete_id
            - payload: decoded jwt payload that has new athlete info
            - athlete_id: Id of athlete to be edited
                - athlete_id is passed through the path. Ex: api/athletes/2 sends
                  patch request for athlete of id=2
            - example post req:
                {
                    "name": "Abby"
                }

        Returns:
            - Status code with json obj of
              the edited athlete in long form in dict
            - Example response:
            @TODO change to approp response.
                {
                    "athletes": [
                        {
                            "id": 2,
                            "recipe": [
                                {
                                    "color": "brown",
                                    "name": "Coffee",
                                    "parts": 1
                                }
                            ],
                            "title": "Decaf"
                        }
                    ],
                    "success": true
                }

        Raises:
            - 404 if no athlete is found with corresponding athlete_id
            - 422 if unable to process request
    """ 
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
  @requires_auth('post:information')
  def create_athlete(payload):
    """ Create a athlete in DB

        Permissions: post:information

        Params: decoded JWT payload with:
            - athlete details
            - required: name, age, city, state, division
             id = db.Column(db.Integer, primary_key=True)
            - example post req:
            @TODO: add post req 
                {
                    "title": "Coffee",
                    "recipe": [{
                        "name": "Coffee",
                        "color": "brown",
                        "parts": 1
                    }]
                }

        Returns:
            - Status code with json obj of
               The new athlete in long form in dict
            - Example response:
            @TODO: add response  
                {
                    "athletes": [
                        {
                            "id": 2,
                            "recipe": [
                                {
                                    "color": "brown",
                                    "name": "Coffee",
                                    "parts": 1
                                }
                            ],
                            "title": "Coffee"
                        }
                    ],
                    "success": true
                }

        Raises:
            - 422 if name, age, city, state, and division are not given in
              payload or unable to process
    """
    data = json.loads(request.data.decode('utf-8'))
    error = False

    name = data.get('name', None)
    age = data.get('age', None)
    city = data.get('city', None)
    state = data.get('state', None)
    phone = data.get('phone', None)
    division = data.get('division', None)

    if not name or not age or not city or not state or not division:
      return jsonify({
            "success": False,
            "error": 422,
            "message": "Name, age, city, state, and division are required."
        }), 422
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
  @requires_auth('delete:information')
  def delete_athlete(payload, athlete_id):
    """ Delete a athlete with id=athlete_id from DB

        Permissions: delete:information

        Params: payload, athlete_id
            - payload: The decoded jwt payload
            - athlete_id: Id of athlete to be edited
                - athlete_id is passed through the path. Ex: /api/athletes/2 sends
                  delete request for athlete of id=2

        Returns:
            - Status code 200 json obj with deleted ID, message,
              and boolean success
            - Example response:
                {
                    "deleted": 2,
                    "message": "athlete deleted successfully",
                    "success": true
                }

        Raises:
            - 404 if no athlete found with corresponding athlete_id
            - 500 if unable to process delete request
    """

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
    """ Get all venues

        Permissions: none required, read only

        Returns:
            - 200 status code with json obj of
              venues in dict.
            - Example response:
            @TODO change to approp response.
                {
                    "drinks": [
                        {
                            "id": 1,
                            "recipe": [
                                {
                                    "color": "blue",
                                    "parts": 1
                                }
                            ],
                            "title": "Water"
                        }
                    ],
                    "success": true
                }

        Raises:
            - 404 if unable to find any corresponding venue
    """
    venues = Venue.query.all()
    print(venues)
    formatted_venues = [venue.format() for venue in venues]
    print(formatted_venues)

    return jsonify({
      'success': True, 
      'venues': formatted_venues
    })

  @app.route('/api/venues/<int:venue_id>', methods=['GET'])
  def get_venue_by_id(venue_id):
    """ Get a particular venue's information

        Permissions: none required, read only

        Returns:
            - 200 status code with json obj of
              venue in dict.
            - Example response:
            @TODO change to approp response.
                {
                    "drinks": [
                        {
                            "id": 1,
                            "recipe": [
                                {
                                    "color": "blue",
                                    "parts": 1
                                }
                            ],
                            "title": "Water"
                        }
                    ],
                    "success": true
                }

        Raises:
            - 404 if unable to find any corresponding venue
    """
    venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
    if venue is None:
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'No such race found in database.'
        }), 404
    formatted_venue = venue.format()
    return jsonify({
      'success': True, 
      'venue': formatted_venue
    })

  @app.route('/api/venues', methods=['POST'])
  @requires_auth('post:information')
  def create_venue(payload): 
    """ Create a athlete in DB

        Permissions: post:information

        Params: decoded JWT payload with:
            - venue details
            - required: name, city, state, address
            - example post req:
            @TODO: add post req 
                {
                    "title": "Coffee",
                    "recipe": [{
                        "name": "Coffee",
                        "color": "brown",
                        "parts": 1
                    }]
                }

        Returns:
            - Status code with json obj of
               The new venue in dict
            - Example response:
            @TODO: add response  
                {
                    "athletes": [
                        {
                            "id": 2,
                            "recipe": [
                                {
                                    "color": "brown",
                                    "name": "Coffee",
                                    "parts": 1
                                }
                            ],
                            "title": "Coffee"
                        }
                    ],
                    "success": true
                }

        Raises:
            - 422 if name, city, state, and address are not given in
              payload or unable to process
    """
    data = json.loads(request.data.decode('utf-8'))
    error = False 

    name = data.get('name', None)
    city = data.get('city', None)
    state = data.get('state', None)
    address = data.get('address', None)

    if not name or not city or not state or not address:
      return jsonify({
            "success": False,
            "error": 422,
            "message": "Name, city, state, and address are required."
        }), 422

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

  @app.route('/api/venues/<int:venue_id>', methods=['PATCH'])
  @requires_auth('patch:information')
  def edit_venue(payload, venue_id):
    """ Edit an venue in DB

        Permissions: patch:information

        Params: payload, venue_id
            - payload: decoded jwt payload that has new venue info
            - venue_id: Id of venue to be edited
                - venue_id is passed through the path. Ex: api/venues/2 sends
                  patch request for venue of id=2
            - example post req:
                {
                    "name": "Sugarloaf"
                }

        Returns:
            - Status code with json obj of
              the edited venue in long form in dict
            - Example response:
            @TODO change to approp response.
                {
                    "venues": [
                        {
                            "id": 2,
                            "recipe": [
                                {
                                    "color": "brown",
                                    "name": "Coffee",
                                    "parts": 1
                                }
                            ],
                            "title": "Decaf"
                        }
                    ],
                    "success": true
                }

        Raises:
            - 404 if no venue is found with corresponding venue_id
            - 422 if unable to process request
    """ 
    data = json.loads(request.data.decode('utf-8'))
    venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
    
    name = data.get('name', None)
    city = data.get('city', None)
    state = data.get('state', None)
    address = data.get('address', None)

    if venue is None: 
      return jsonify({
        'success': False, 
        'error': 404,
        'message': 'No such athlete found in database.'
      }), 404
    
    try: 
      if name:
        venue.name = name 
      if city:
        venue.city = city 
      if state:
        venue.state = state 
      if address:
        venue.address = address

      venue.update()
      return jsonify({
            'success': True
        }), 200

    except Exception as error_msg:
        print(error_msg)
        abort(422)

  @app.route('/api/venues/<int:venue_id>', methods=['DELETE'])
  @requires_auth('delete:information')
  def delete_venue(payload, venue_id):
    """ Delete a venue with id=venue_id from DB

        Permissions: delete:informatioon

        Params: payload, venue_id
            - payload: The decoded jwt payload
            - venue_id: Id of venue to be edited
                - venue_id is passed through the path. Ex: /api/venues/2 sends
                  delete request for venue of id=2

        Returns:
            - Status code 200 json obj with deleted ID, message,
              and boolean success
            - Example response:
                {
                    "deleted": 2,
                    "message": "venue deleted successfully",
                    "success": true
                }

        Raises:
            - 404 if no venue found with corresponding venue_id
            - 500 if unable to process delete request
    """ 
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
    formatted_races = [race.format() for race in races]
    
    for comp in formatted_races: 
      rs = Athlete.query.join(racers).join(Race).filter((racers.c.racer_id == Athlete.id) & (racers.c.race_id == Race.id) & (racers.c.race_id == comp['id'])).all()
      venue = Venue.query.filter(Venue.id == comp['venue_id']).one_or_none()
      formatted_venue = venue.format()
      formatted_racers = [racer.format() for racer in rs]
      comp['racers'] = formatted_racers
      comp['venue'] = formatted_venue

    return jsonify({
      'success': True, 
      'races': formatted_races,
    })

  # @app.route('/api/races/<int:race_id>', methods=['GET'])
  # def get_race_by_id(race_id):
  #   race = Race.query.filter(Race.id == race_id).one_or_none()
  #   if race is None:
  #       return jsonify({
  #           'success': False,
  #           'error': 404,
  #           'message': 'No such race found in database.'
  #       }), 404

    

    
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
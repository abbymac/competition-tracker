import os
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
  print('hi there')
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
  
  @app.route('/athletes', methods=['GET'])
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

  @app.route('/athletes', methods=['POST'])
  def create_athlete(): 
    data = json.loads(request.data.decode('utf-8'))
   
    error = False

    new_name = data.get('name', None)
    new_age = data.get('age', None)
    new_city = data.get('city', None)
    new_state = data.get('state', None)
    new_phone = data.get('phone', None)
    new_division = data.get('division', None)
    new_races = data.get('races', None)

    try: 
      athelete = Athlete(
        question=new_question,
        answer=new_answer,
        category=new_category,
        difficulty=new_difficulty
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


  # Venues
  @app.route('/venues', methods=['GET'])
  def get_venues(): 
    print('in here')
    venues = Venue.query.all()
    print(venues)
    formatted_venues = [venue.format() for venue in venues]
    print(formatted_venues)

    return jsonify({
      'success': True, 
      'venues': formatted_venues
    })


  # Races

  @app.route('/races', methods=['GET'])
  def get_races(): 
    print('in here')
    races = Race.query.all()
    # print(races)


    
    # formatted_races = [race.format() for race in races]
    # print(formatted_races)
    def format(racer): 
      # print('racer', racer)
      # return { 
      #   'racer_id': racer.id,
      #   ''
      # }
      # for e, i in racer.__dict__.items(): 
      #   print('e is', e)
      #   print('i is', i)

      return  {
        'racer_id': racer.id,
        'name': racer.name,
        'city': racer.city, 
        'phone': racer.phone, 
        'state': racer.state, 
        'division': racer.division       
      }
    # formatted_races = [format(race) for race in races]

    rs = Athlete.query.join(racers).join(Race).filter((racers.c.racer_id == Athlete.id) & (racers.c.race_id == Race.id)).all()
    # print('t', rs)
    race_athletes = []
    for x in rs: 
      # print('x is', x)
      form = format(x)
      race_athletes.append(form)
      print('something', race_athletes)
    data = {}
    # for race in formatted_races: 
    #   r = racers.query.filter(race_id == race.id)
    #   print('r is', r)
    # print('after', r)

    return jsonify({
      'success': True, 
      # 'races': formatted_races,
      'racer_athletes': race_athletes
    })



  return app




APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
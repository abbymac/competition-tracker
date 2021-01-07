import os
import sys
import json

from flask import (
  Flask,
  render_template,
  request,
  Response,
  flash,
  redirect,
  jsonify,
  abort
)
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
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
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
                {
                  "athletes": [
                      {
                          "age": 23,
                          "city": "Portland",
                          "division": "elite",
                          "id": 2,
                          "name": "Emma",
                          "phone": "2071234567",
                          "state": "ME"
                      },
                      {
                          "age": 24,
                          "city": "CE",
                          "division": "elite",
                          "id": 1,
                          "name": "Heidi",
                          "phone": null,
                          "state": "ME"
                      },
                  ],
                  "success": true
              }

        """

        athletes = Athlete.query.all()

        formatted_athletes = [athlete.format() for athlete in athletes]

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
                    - athlete_id is passed through the path.
                      Ex: api/athletes/2 sends
                      patch request for athlete of id=2
                - example post req:
                    {
                        "name": "Abby"
                    }

            Returns:
                - Status code with json obj of
                  the edited athlete in dict
                - Example response:
                  {
                      "athlete": {
                          "age": 24,
                          "city": "CE",
                          "division": "elite",
                          "id": 1,
                          "name": "Jay",
                          "phone": null,
                          "state": "ME"
                      },
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
            formatted_athlete = athlete.format()

            return jsonify({
                'athlete': formatted_athlete,
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
                - example post req:
                    {
                        "age": 32,
                        "city": "Burlington",
                        "division": "elite",
                        "name": "Lex",
                        "phone": "1213445989",
                        "state": "VT"
                    }

            Returns:
                - Status code with json obj of
                   The new athlete in formatted dict
                - Example response:
                    {
                        "athlete": {
                            "age": 32,
                            "city": "Burlington",
                            "division": "elite",
                            "id": 10,
                            "name": "Lex",
                            "phone": "1213445989",
                            "state": "VT"
                        },
                        "message": "Athlete created successfully",
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
        except BaseException:
            error = True
            db.session.rollback()
            print(sys.exc_info)
        finally:
            new_athlete = athlete.format()
            db.session.close()
        if error:
            abort(422)
            flash('An error occured. Athlete unsuccessfully created.')
        else:
            return jsonify({
                'athlete': new_athlete,
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
                    - athlete_id is passed through the path.
                      Ex: /api/athletes/2 sends
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
        except BaseException:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
        if error:
            print('test fail at delete')
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
                    {
                        "success": true,
                        "venues": [
                            {
                                "address": "1 main street",
                                "city": "CV",
                                "id": 1,
                                "name": "Sugarloaf",
                                "state": "ME"
                            }
                        ]
                    }

        """
        venues = Venue.query.all()
        formatted_venues = [venue.format() for venue in venues]

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
                    {
                        "success": true,
                        "venue":
                            {
                                "address": "1 main street",
                                "city": "CV",
                                "id": 1,
                                "name": "Sugarloaf",
                                "state": "ME"
                            }
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
                {
                    "name": "Sunday River",
                    "city": "Bethel",
                    "state": "VT",
                    "address": "6 main street"
                }

            Returns:
                - Status code with json obj of
                   The new venue in dict
                - Example response:
                {
                    "message": "venue create successfully",
                    "new_venue": {
                        "address": "6 main street",
                        "city": "Bethel",
                        "id": 8,
                        "name": "Sunday River",
                        "state": "VT"
                    },
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
                name=name,
                city=city,
                state=state,
                address=address
            )
            venue.insert()
            venue.update()
        except BaseException:
            error = True
            db.session.rollback()
            print(sys.exc_info)
        finally:
            new_venue = venue.format()
            db.session.close()
        if error:
            abort(422)
        else:
            return jsonify({
                'new_venue': new_venue,
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
                    - venue_id is passed through the path.
                      Ex: api/venues/2 sends
                      patch request for venue of id=2
                - example post req:
                    {
                        "name": "Sugarloaf"
                    }

            Returns:
                - Status code with json obj of
                  the edited venue in long form in dict
                - Example response:
                {
                    "success": true,
                    "venue": {
                        "address": "7 main street",
                        "city": "CV",
                        "id": 1,
                        "name": "Sugarloaf",
                        "state": "ME"
                    }
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
                'message': 'No such venue found in database.'
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
                'venue': venue.format(),
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
                    - venue_id is passed through the path.
                    Ex: /api/venues/2 sends
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
        venue = Venue.query.filter(Venue.id == venue_id).one_or_none()

        if venue is None:
            return jsonify({
                'success': False,
                'error': 404,
                'message': 'No such venue found in database.'
            }), 404

        try:
            venue.delete()
        except BaseException:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
        if error:
            print('error at venue')
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
        """ Get all races

            Permissions: none

            Params: none

            Returns:
              - success
              - example response:
              {
                "races": [
                    {
                        "division": "elite",
                        "id": 4,
                        "name": "classic",
                        "prize": 1000,
                        "racers": [
                            {
                                "age": 24,
                                "city": "CE",
                                "division": "elite",
                                "id": 1,
                                "name": "Jay",
                                "phone": null,
                                "state": "ME"
                            },
                            {
                                "age": 23,
                                "city": "Portland",
                                "division": "elite",
                                "id": 2,
                                "name": "Emma",
                                "phone": "2071234567",
                                "state": "ME"
                            }
                        ],
                        "start_time": "Fri, 28 Sep 2001 01:00:00 GMT",
                        "venue": {
                            "address": "7 main street",
                            "city": "CV",
                            "id": 1,
                            "name": "Sugarloaf",
                            "state": "ME"
                        },
                        "venue_id": 1
                    },
                    {
                        "division": "elite",
                        "id": 6,
                        "name": "classic",
                        "prize": 1000,
                        "racers": [],
                        "start_time": "Fri, 18 Dec 2020 18:45:01 GMT",
                        "venue": {
                            "address": "7 main street",
                            "city": "CV",
                            "id": 1,
                            "name": "Sugarloaf",
                            "state": "ME"
                        },
                        "venue_id": 1
                    }
                ],
                "success": true
            }

        """
        races = Race.query.all()
        formatted_races = [race.format() for race in races]

        for comp in formatted_races:
            rs = Athlete.query.join(racers).join(Race).filter(
                (racers.c.racer_id == Athlete.id) & (
                    racers.c.race_id == Race.id) & (
                    racers.c.race_id == comp['id'])).all()
            venue = Venue.query.filter(
                Venue.id == comp['venue_id']).one_or_none()
            formatted_venue = venue.format()
            formatted_racers = [racer.format() for racer in rs]
            comp['racers'] = formatted_racers
            comp['venue'] = formatted_venue

        return jsonify({
            'success': True,
            'races': formatted_races,
        })


# --------------------------------------------------------------------------------------------------------
# Error Handling
# --------------------------------------------------------------------------------------------------------

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def unproccesable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=process.env.PORT, debug=True)

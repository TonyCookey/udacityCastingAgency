import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # Index route with API Information
  @app.route('/')
  def index():
    return jsonify({
      'API': 'Casting Agency API',
      'API-Name': 'Premiere API',
      'API Description': 'API for managing Actors and Movies information',
      'Author': 'Tony Cookey'
    })

  # Get all Actors in the Database
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(payload):
    data = []
    actors = Actor.query.all()
    if actors is not None:
      for actor in actors:
        data.append(actor.format())
    
    return jsonify({
      'success':True,
      'actors': data
    })

  # Get all Movies in the Database
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(payload):
    data = []
    movies = Movie.query.all()
    if movies is not None:
      for movie in movies:
        data.append(movie.format())
    
    return jsonify({
      'success':True,
      'movies': data
    })

  # Create/Insert new Movie into the Database
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(payload):
    data = []
    body = request.get_json()
    if 'title' not in body or 'release_date' not in body:
      abort(422, description='unprocessable, request fields are empty')
    title = body['title']
    release_date = body['release_date']

    if title is None or release_date is None:
      abort(422, description="Unprocessable. Request fields are null")
    movie = Movie(title=title, release_date=release_date)
    movie.insert()

    inserted_movie = Movie.query.get(movie.id)
    if inserted_movie is None:
      abort(404, description="Could not find Movie")
    data.append(inserted_movie.format())
    return jsonify({
      'success': True,
      'movie': data
    })  

  
  # Create/Insert New Actor into the Database
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(payload):
    data = []
    body = request.get_json()
    if 'name' not in body:
      abort(422, description='unprocessable, name field is empty')
    if 'age' not in body:
      abort(422, description='unprocessable, age field is empty')
    if 'gender' not in body:
      abort(422, description='unprocessable, gender field is empty')
    
    name = body['name']
    age = body['age']
    gender = body['gender']

    if name is None:
      abort(422, description="Unprocessable. name field is null")
    if age is None:
      abort(422, description="Unprocessable. age field is null")
    if gender is None:
      abort(422, description="Unprocessable. gender field is null")
    actor = Actor(name=name, age=age, gender=gender)
    actor.insert()

    inserted_actor = Actor.query.get(actor.id)
    if inserted_actor is None:
      abort(404, description="Could not find actor")
    data.append(inserted_actor.format())
    return jsonify({
      'success': True,
      'actor': data
    })
  
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, id):    
    data = []
    body = request.get_json()
    movie = Movie.query.get(id)    
    # check if the Movie exists
    if movie is None:
      abort(404, description="could not find Movie")
    if 'title' in body:
      title = request.get_json()['title']
      movie.title = title
    # check if the recipe field is present on the request body
    if 'release_date' in body:
      release_date = request.get_json()['release_date']
      movie.release_date = release_date
    # check if both fields are not present on the request body
    if 'title' not in body and 'release_date' not in body:
      abort(400, description="requires at least one field to update")
    # update movie details
    movie.update()
    # get updated movie
    updated_movie = Movie.query.get(id)
    # check if updated movie details persisted
    if updated_movie is None:
      abort(404)
    # format he movie object using long() and append to an array
    
    data.append(updated_movie.format())
    return jsonify({
      'success': True,
      'movie': data
    })
   
  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, id):    
    data = []
    body = request.get_json()
    actor = Actor.query.get(id)    
    # check if the actor exists
    if actor is None:
      abort(404, description="could not find actor")
    if 'name' in body:
      name = request.get_json()['name']
      actor.name = name

    # check if the age field is present on the request body
    if 'age' in body:
      age = request.get_json()['age']
      actor.age = age

    if 'gender' in body:
      gender = request.get_json()['gender']
      actor.gender = gender

    # check if all fields are not present on the request body
    if 'name' not in body and 'age' not in body and 'gender' not in body:
      abort(400, description="requires at least one field to update")
    # update actor details
    actor.update()
    # get updated actor
    updated_actor = actor.query.get(id)
    # check if updated actor details persisted
    if updated_actor is None:
      abort(404)
    # format the actor object using format() and append to an array    
    data.append(updated_actor.format())
    return jsonify({
      'success': True,
      'actor': data
    })

  # Delete actor using the actor id
  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, id):
    actor = Actor.query.get(id)
    if actor is None:
      abort(404, description="Cannot delete, Actor does not exist")
    actor.delete()
    return jsonify({
      'success':True,
      'deleted': id
    })
  # Delete movie using the movie id
  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, id):
    movie = Movie.query.get(id)
    if movie is None:
      abort(404, description="Cannot delete, movie does not exist")
    movie.delete()
    return jsonify({
      'success':True,
      'deleted': id
    })  


  # Define Error Handlers
  # Error handler for 400
  @app.errorhandler(400)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": error.description
    }), 400 

  # Error hadler for 404
  @app.errorhandler(404)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": error.description
    }), 404

  # Error handler for 405
  @app.errorhandler(405)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": 'Method Not Allowed'
    }), 405

  # Error handler for 422
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": error.description
    }), 422

  @app.errorhandler(500)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
    }), 500

  @app.errorhandler(AuthError)
  def unauthorized(e):
    return jsonify({
      "success": False,
      "error": e.status_code,
      "description": e.error["description"],
      "code": e.error["code"],
    }), e.status_code

  return app

APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
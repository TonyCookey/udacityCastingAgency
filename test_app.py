import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


# casting_assistant_token = os.environ.get('CASTING_ASSISTANT_TOKEN')
casting_assistant_token = os.environ.get('CASTING_ASSISTANT_TOKEN')
casting_director_token = os.environ.get('CASTING_DIRECTOR_TOKEN')
executive_director_token = os.environ.get('EXECUTIVE_DIRECTOR_TOKEN')

class CastingAgencyTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.database_path = os.environ.get('SQLALCHEMY_DATABASE_URI_TEST')
    setup_db(self.app, self.database_path)
    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()
    self.casting_assistant_bearer_token = {
      "Authorization" : "Bearer {}".format(casting_assistant_token)
    }
    self.casting_director_bearer_token = {
      "Authorization" : "Bearer {}".format(casting_director_token)
    } 
    self.executive_director_bearer_token = {
      "Authorization" : "Bearer {}".format(executive_director_token)
    }
    self.new_actor = {
      "name" : "Tony Cookey",
      "age" : 32,
      "gender": "Male"
    }    
    self.update_actor = {
      "name" : "Anthony Cookey"
    }    
    self.new_movie = {
      "title" : "The Rock",
      "release_date" : "2019-06-23"    
    }    
    self.update_movie = {
      "title" : "The Rock 2"
    }    
  def tearDown(self):
    pass

  # Test Endpoints for Executive Director
  def test_get_all_movies_executive_director(self):
    res = self.client().get('/movies', headers=self.executive_director_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertIsInstance(data['movies'], list)
    self.assertEqual(data['success'], True)
  
  def test_get_all_actors_executive_director(self):
    res = self.client().get('/actors', headers=self.executive_director_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertIsInstance(data['actors'], list)
    self.assertEqual(data['success'], True)

  def test_post_actor_executive_director(self):
    res = self.client().post('/actors', headers=self.executive_director_bearer_token, json=self.new_actor)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertIsInstance(data['actor'], list)
    self.assertEqual(data['success'], True)
  
  def test_length_response_post_actor_executive_director(self):
    res = self.client().post('/actors', headers=self.executive_director_bearer_token, json=self.new_actor)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertIsInstance(data['actor'], list)
    self.assertEqual(len(data['actor']), 1)
  
  def test_422_post_actor_executive_director(self):
    res = self.client().post('/actors', headers=self.executive_director_bearer_token, json={})
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)

 
  def test_post_movie_executive_director(self):
    res = self.client().post('/movies', headers=self.executive_director_bearer_token, json=self.new_movie)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)

  def test_response_post_movie_executive_director(self):
    res = self.client().post('/movies', headers=self.executive_director_bearer_token, json=self.new_movie)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertIsInstance(data['movie'], list)

  def test_422_post_movie_executive_director(self):
    res = self.client().post('/movies', headers=self.executive_director_bearer_token, json={})
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)

  
  
  # Test Endpoints for Casting Assistants
  def test_get_all_movies_casting_assistant(self):
    res = self.client().get('/movies', headers=self.casting_assistant_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertIsInstance(data['movies'], list)
  
  def test_get_all_actors_casting_assistant(self):
    res = self.client().get('/actors', headers=self.casting_assistant_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertIsInstance(data['actors'], list)

  def test_401_post_actor_casting_assistant(self):
    res = self.client().post('/actors', headers=self.casting_assistant_bearer_token, json=self.new_actor)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 401)
    self.assertEqual(data['success'], False)
 
  def test_401_post_movie_casting_assistant(self):
    res = self.client().post('/movies', headers=self.casting_assistant_bearer_token, json=self.new_movie)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 401)
    self.assertEqual(data['success'], False)

  def test_401_patch_actor_casting_assistant(self):
    res = self.client().patch('/actors/1', headers=self.casting_assistant_bearer_token, json=self.update_actor)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 401)
    self.assertEqual(data['success'], False)

  def test_401_patch_movie_casting_assistant(self):
    res = self.client().patch('/movies/1', headers=self.casting_assistant_bearer_token, json=self.update_movie)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 401)
    self.assertEqual(data['success'], False)

  def test_401_delete_movie_casting_assistant(self):
    res = self.client().delete('/movies/1', headers=self.casting_assistant_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 401)
    self.assertEqual(data['success'], False)
  
  def test_401_delete_actors_casting_assistant(self):
    res = self.client().delete('/actors/1', headers=self.casting_assistant_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 401)
    self.assertEqual(data['success'], False)
  
  
  # Test Endpoints for Casting Assistants
  def test_get_all_movies_casting_director(self):
    res = self.client().get('/movies', headers=self.casting_director_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertIsInstance(data['movies'], list)
  
  def test_get_all_actors_casting_director(self):
    res = self.client().get('/actors', headers=self.casting_director_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertIsInstance(data['actors'], list)
  

  def test_post_actor_casting_director(self):
    res = self.client().post('/actors', headers=self.casting_director_bearer_token, json=self.new_actor)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertIsInstance(data['actor'], list)
    self.assertTrue(len(data['actor']), 1)  
   
 
  def test_401_post_movie_casting_director(self):
    res = self.client().post('/movies', headers=self.casting_director_bearer_token, json=self.new_movie)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 401)
    self.assertEqual(data['success'], False)

  def test_401_delete_movie_casting_director(self):
    res = self.client().delete('/movies/1', headers=self.casting_director_bearer_token, json=self.new_movie)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 401)
    self.assertEqual(data['success'], False)


  # Tests for Patch and Deletes

  def test_patch_actor_executive_director(self):
    res = self.client().patch('/actors/2', headers=self.executive_director_bearer_token, json=self.update_actor)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertIsInstance(data['actor'], list)
  
  def test_400_patch_actor_executive_director(self):
    res = self.client().patch('/actors/2', headers=self.executive_director_bearer_token, json={})
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['success'], False)

  def test_404_patch_actor_executive_director(self):
    res = self.client().patch('/actors/1000', headers=self.executive_director_bearer_token, json=self.update_actor)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)

  def test_404_patch_movie_executive_director(self):
    res = self.client().patch('/movies/1000', headers=self.executive_director_bearer_token, json=self.update_movie)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False) 

  def test_delete_movie_executive_director(self):
    res = self.client().delete('/movies/2', headers=self.executive_director_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['deleted'])
  
  def test_404_delete_movie_executive_director(self):
    res = self.client().delete('/movies/10000', headers=self.executive_director_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
  
  def test_delete_actors_executive_director(self):
    res = self.client().delete('/actors/2', headers=self.executive_director_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
  
  def test_404_delete_actors_executive_director(self):
    res = self.client().delete('/actors/1000', headers=self.executive_director_bearer_token)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
  

 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
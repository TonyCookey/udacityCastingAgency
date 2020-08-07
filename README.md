# Casting Agency API

## Getting Started
This is a Casting Agency API which returns a directory of Movies and Actors associated with this Casting Agency. This API allows the Agency to manage Actors and Movies. The API makes use of Authentication which gives certain roles access to certain functionalities. This project is the final project of my Full stack Web Developer Nano Degree Program. I enjoyed building it and I hope you enjoy using it.

## LIVE URL : https://still-citadel-94091.herokuapp.com/

## Tech Stack
This is a Python Flask Application which uses and utilizes a Postgres Database
- Python
- Flask
- Postgres SQL

### Installing Dependencies

#### Python 3.7 - 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python). (Preferrably Python 3.8)

#### Virtual Enviornments

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) or you can utilize the steps below.

##### Set up a Virtual Enviornment

To create a virtual environment, go to your project’s directory and run venv. If you are using Python 2, replace venv with virtualenv in the below commands.

On macOS and Linux:
```bash
python3 -m venv env
```
On Windows:
```bash
py -m venv env
```


##### Activate a Virtual Enviornment

On macOS and Linux:
```bash
source env/bin/activate
```
On Windows:
```bash
.\env\Scripts\activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the **root directory** and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.


##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.


### Setting Up Project Locally

After succesfully installing all requirements for the project. You can setup the project locally by following the steps below:

1. Create Databases. You need to create two databases. You can create databases by either using a Postgrest Client (PG Admin) or using the createdb engine. The first database is the actual database for the appliation, while the second is the test database for running tests
```
createdb castingAgency
createdb CastingAgencyTest
```


2. Configure the setup.sh with appropiate variables. *Make sure to set the SQLALCHEMY_DATABASE_URI and the SQLALCHEMY_DATABASE_URI_TEST correctly by inputing the correct database username and password*. 
```
export SQLALCHEMY_DATABASE_URI='postgresql://<username>:<password>@localhost:5432/castingAgency'
export SQLALCHEMY_DATABASE_URI_TEST='postgresql://<username>:<password>@localhost:5432/castingAgencyTest'
```

3. Expose Credentials to Enviroment after succesful configuration of setup.sh file. *The credentials in the setup.sh are used by the app and are very neccesary to running the app. Run the command below. Running this command in a virtual enviroment is preferable*
```
source setup.sh
```
4. Run the application by using the command below
```
flask run
```

### API Endpoints
Listed below are the Endpoints in the system
- GET /
- GET /actors
- GET /movies
- POST /actors
- POST /movies
- PATCH /actors/<int:id>
- PATCH /movies/<int:id>
- DELETE /actors/<int:id>
- DELETE /movies/<int:id>


#### Roles and Endpoints (RBAC Controls)
This API has Three Roles which have different differet access to endpoints. Listed below are the accesible and allowed endpoints for each user. Each request must be sent with an Authorization Header which is a Bearer Token
```
 "Authorization" : "Bearer (TOKEN)"
```

- Casting Assistant
  - GET /
  - GET /actors
  - GET /movies
  
- Casting Director
  - GET /
  - GET /actors
  - GET /movies
  - POST /actors
  - PATCH /actors/<int:id>
  - PATCH /movies/<int:id>
  - DELETE /actors/<int:id>
 
- Executive Director
  - GET /
  - GET /actors
  - GET /movies
  - POST /actors
  - POST /movies
  - PATCH /actors/<int:id>
  - PATCH /movies/<int:id>
  - DELETE /actors/<int:id>
  - DELETE /movies/<int:id>



### API Endpoints Behaviour

#### GET /
- Description: Returns Information about the API
- request argument: None
- Example Response: 
```
{
  "API": "Casting Agency API",
  "API Description": "API for managing Actors and Movies information",
  "API-Name": "Premiere API",
  "Author": "Tony Cookey"
}
```

#### GET /actors
- Description: Return a list of all actors in the Database
- Request argument: None
- Example Response: 
```
{
  "actors": [
    {
      "age": 38,
      "gender": "Male",
      "id": 1,
      "name": "Neil Patrick Harris"
    },
    {
      "age": 40,
      "gender": "Male",
      "id": 2,
      "name": "Kevin Hart"
    },
    {
      "age": 41,
      "gender": "Female",
      "id": 3,
      "name": "Mila Kunis"
    },
    {
      "age": 45,
      "gender": "Female",
      "id": 4,
      "name": "Sofia Vegara"
    },
    {
      "age": 40,
      "gender": "Female",
      "id": 5,
      "name": "Jessica Alba"
    }
  ],
  "success": true
}
```
#### GET /movies
- Description: Return a list of all movies in the Database
- Request argument: None
- Example Response:
```
{
  "actors": [
    {
      "age": 38,
      "gender": "Male",
      "id": 1,
      "name": "Neil Patrick Harris"
    },
    {
      "age": 40,
      "gender": "Male",
      "id": 2,
      "name": "Kevin Hart"
    },
    {
      "age": 41,
      "gender": "Female",
      "id": 3,
      "name": "Mila Kunis"
    },
    {
      "age": 45,
      "gender": "Female",
      "id": 4,
      "name": "Sofia Vegara"
    },
    {
      "age": 40,
      "gender": "Female",
      "id": 5,
      "name": "Jessica Alba"
    }
  ],
  "success": true
}
```
#### POST /actors
- Description: Create a new Actor, Insert a new actor into the Database
- Request argument: None
- Request Body : 
```
{
    "name": "Jessica Alba",
    "age": 40,
    "gender": "Female"
}
```
- Example Response:
```
{
  "actor": [
    {
      "age": 40,
      "gender": "Female",
      "id": 5,
      "name": "Jessica Alba"
    }
  ],
  "success": true
}
```

#### POST /movies
- Description: Create a new Movie, Insert a new movie into the Database
- Request argument: None
- Request Body :
```
{
    "title": "Think Like a Man",
    "release_date": "2017-05-19"
}
```
- Example Response:
```
{
  "movie": [
    {
      "id": 5,
      "release_date": "Fri, 19 May 2017 00:00:00 GMT",
      "title": "Think Like a Man"
    }
  ],
  "success": true
}
```

#### PATCH /movies/<int:id>
- Description: Update an existing Movie details
- Request argument: ID - Movie ID - 1
- Request Body : the title or the release date, Any or Both of these fields can be updated
```
{
    "title": "The Matrix II"
}
```
- Example Response:
```
{
  "movie": [
    {
      "id": 1,
      "release_date": "Thu, 27 Aug 2020 00:00:00 GMT",
      "title": "The Matrix II"
    }
  ],
  "success": true
}
```

#### PATCH /actors/<int:id>
- Description: Update an existing Actor's Details using the Actor's ID
- Request argument: ID - Actor ID - 1
- Request Body : the Name or the Age or the Gender, any or all of them can be updated
```
{
    "age": 39
}
```
- Example Response:
```
{
  "actor": [
    {
      "age": 39,
      "gender": "Male",
      "id": 1,
      "name": "Neil Patrick Harris"
    }
  ],
  "success": true
}
```

#### DELETE /actors/<int:id>
- Description: Delete an existing Actor using the Actor's ID
- Request argument: ID - Actor ID - 1
- Request Body : None
- Example Response:
```
{
  "deleted": 1,
  "success": true
}
```

#### DELETE /movies/<int:id>
- Description: Delete an existing Movie using the Movie's ID
- Request argument: ID - Movie ID - 1
- Request Body : None
- Example Response:
```
{
  "deleted": 1,
  "success": true
}
```
### Testing the Application Locally
You can carry out unit tests on the application by following the steps below:

1. Create Test Database- Skip this step if you already created and configured the test DB earlier

2. Populate the Test Database using psql by running the command below. This will populate the Test DB with data defined in the test_db file
```
psql castingAgencyTest < test_db

```

3. Run Test
```
python test_app.py
```


## Enviroment Variables
The Auth Tokens for Testing the Application are located in the setup.sh file
- Casting Assistant: CASTING_ASSISTANT_TOKEN
- Casting Director: CASTING_DIRECTOR_TOKEN
- Executive Director: EXECUTIVE_DIRECTOR_TOKEN

The Database URL for both the Actual and Test Applications are also located in the setup.sh file
- Live Database URL: SQLALCHEMY_DATABASE_URI
- Test Database URL: SQLALCHEMY_DATABASE_URI_TEST

## Hosting
This Application is hosted on Heroku  
**Live URL** : https://still-citadel-94091.herokuapp.com/


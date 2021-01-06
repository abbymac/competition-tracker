---

## Introduction

For the Capstone project for Fullstack Development Nano Degree, I decided to build a program to manage and track various races. As a former athlete in national snowboard competitions, I wanted to build something that relates to real experiences I have had.

## Overview

## Tech Stack (Dependencies)

### 1. Backend Dependencies

The tech stack includes the following:

- **virtualenv** as a tool to create isolated Python environments
- **SQLAlchemy ORM** to be our ORM library of choice
- **PostgreSQL** as our database of choice
- **Python3** and **Flask** as our server language and server framework
- **Flask-Migrate** for creating and running schema migrations
  You can download and install the dependencies mentioned above using `pip` as:

```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

> **Note** - If we do not mention the specific version of a package, then the default latest stable package will be installed.

### 2. Frontend Dependencies

Frontend displays data

Install dependencies with

```
npm install
```

```
node -v
npm -v
```

## Development Setup

1. **Download the project starter code locally**

```
git clone https://github.com/abbymac/capstone.git
cd capstone
```

2. **Initialize and activate a virtualenv using:**

```
python -m virtualenv env
source env/bin/activate
```

> **Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:

```
source env/Scripts/activate
```

4. **Install the dependencies:**

```
pip install -r requirements.txt
```

5. **Run the development server:**

```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

# API Reference

## Getting Started

- Base URL:

- Authentication: Authentication is operated through Auth0. The roles exist as such:

#### Spectator

Spectator role is read only. It can only fetch information, but is not authorized to edit, create, or delete anything.

#### Organizer

An organizer has all edit access. It can create, edit, and delete new athletes, venues, and races.

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
	"success": False,
  "error": 400,
  "message": "Bad request"
}

```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Unprocessable entity
- 500: Internal Server Error

## Endpoints

### GET '/api/athletes'

- Get all athletes from DB
- Permissions: none.
- Returns: 200 status code with json obj of athletes in dict
- Sample returned object:

```
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
```

### DELETE 'api/athletes/<int:athlete_id>'

- Delete a athlete with id=athlete_id from DB
- Permissions: requires delete:information permission
- Request Argument: payload, 'athlete_id'. Where ID is an integer
- Returns: an object with keys: 'deleted', 'message', 'success'
- Sample returned object:

```
{
    "deleted": 2,
    "message": "athlete deleted successfully",
    "success": true
}
```

Raises:

- 404 if no athlete found with corresponding athlete_id
- 500 if unable to process delete request

### POST '/questions'

- Create new question
- Request Argument: none
- Requires: a question object

Sample returned object:

```
	{
    	'success': True,
        'message': 'Question created successfully'
    }
```

### POST '/api/athletes'

- Create a athlete in DB.
- Params: decoded JWT payload with:
  - athlete details
  - required: name, age, city, state, division
  - example post req:
  ```
       {
           "age": 32,
           "city": "Burlington",
           "division": "elite",
           "name": "Lex",
           "phone": "1213445989",
           "state": "VT"
       }
  ```
- Returns: Status code with json obj of the new athlete in formatted dict

Sample returned object:

```
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

```

Raises:

- 422 if name, age, city, state, and division are not given in
  payload or unable to process

### PATCH '/api/athletes/<int:athlete_id>

- Edit an athlete in DB
- Permissions: patch:information
- Params: payload, athlete_id
  - payload: decoded jwt payload that has new athlete info
  - athlete_id: Id of athlete to be edited
    - athlete_id is passed through the path.
      Ex: api/athletes/2 sends
      patch request for athlete of id=2
  - example post req:
  ```
  {
      "name": "Abby"
  }
  ```
- Returns: Status code with json obj of the edited athlete in dict

Sample object returned with athlete_id=1

```
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

```

Raises:

- 404 if no athlete is found with corresponding athlete_id
- 422 if unable to process request

### GET '/api/venues'

- Get all venues from DB
- Permissions: none.
- Returns: 200 status code with json obj of athletes in dict
- Sample returned object:

```
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
```

# Superhero-code-challenge
This is a Flask API for managing heroes and their powers.

## Setup
1. Clone the repo and navigate to the project folder:
   git clone <repo-url>
   cd supeheronames/server
2. Install dependencies:
    pipenv install
    pipenv shell
3. Set up the database:
    export FLASK_APP=app.py
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    python seed.py
4. Run the server:
    flask run

**Endpoints**
GET /heroes
Returns all heroes.

GET /heroes/<id>
Returns details of one hero.

GET /powers
Returns all powers.

GET /powers/<id>
Returns details of one power.

PATCH /powers/<id>
Updates power description (min 20 characters).

POST /hero_powers
Assigns a power to a hero.

Error Handling
404 for not found resources
400 for validation errors
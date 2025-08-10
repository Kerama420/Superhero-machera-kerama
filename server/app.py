# server/app.py
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from config import config 
from models import Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Welcome route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Superheroes API"})

# GET all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_list = [
        {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
        for hero in heroes
    ]
    return jsonify(heroes_list)

# GET hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": [
            {
                "id": hp.power.id,
                "name": hp.power.name,
                "description": hp.power.description
            }
            for hp in hero.hero_powers
        ]
    }
    return jsonify(hero_data)

# GET all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_list = [
        {"id": power.id, "name": power.name, "description": power.description}
        for power in powers
    ]
    return jsonify(powers_list)

# GET power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    return jsonify({
        "id": power.id,
        "name": power.name,
        "description": power.description
    })

# PATCH update power description
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    if "description" not in data or len(data["description"]) < 20:
        return jsonify({"errors": ["description must be at least 20 characters long"]}), 400

    power.description = data["description"]
    db.session.commit()

    return jsonify({
        "id": power.id,
        "name": power.name,
        "description": power.description
    })

# POST create hero_power relationship
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    try:
        new_hero_power = HeroPower(
            strength=data["strength"],
            hero_id=data["hero_id"],
            power_id=data["power_id"]
        )
        db.session.add(new_hero_power)
        db.session.commit()

        hero = Hero.query.get(data["hero_id"])
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {
                    "id": hp.power.id,
                    "name": hp.power.name,
                    "description": hp.power.description
                }
                for hp in hero.hero_powers
            ]
        }
        return jsonify(hero_data), 201
    except Exception:
        return jsonify({"errors": ["validation errors"]}), 400

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .models import Hero, Power, HeroPower

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Superheroes API"})

    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        return jsonify([h.to_dict() for h in heroes])

    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero(id):
        hero = Hero.query.get(id)
        if not hero:
            return jsonify({"error": "Hero not found"}), 404
        return jsonify({
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "hero_powers": [
                {
                    "id": hp.id,
                    "hero_id": hp.hero_id,
                    "power_id": hp.power_id,
                    "strength": hp.strength,
                    "power": {
                        "id": hp.power.id,
                        "name": hp.power.name,
                        "description": hp.power.description
                    }
                }
                for hp in hero.hero_powers
            ]
        })

    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        return jsonify([p.to_dict() for p in powers])

    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power(id):
        power = Power.query.get(id)
        if not power:
            return jsonify({"error": "Power not found"}), 404
        return jsonify(power.to_dict())

    @app.route('/powers/<int:id>', methods=['PATCH'])
    def patch_power(id):
        from flask import request
        power = Power.query.get(id)
        if not power:
            return jsonify({"error": "Power not found"}), 404
        data = request.get_json() or {}
        desc = data.get('description')
        if not desc or len(desc) < 20:
            return jsonify({"errors": ["description must be at least 20 characters long"]}), 400
        power.description = desc
        db.session.commit()
        return jsonify(power.to_dict())

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        from flask import request
        data = request.get_json() or {}
        strength = data.get('strength')
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')
        if strength not in ('Strong', 'Weak', 'Average'):
            return jsonify({"errors": ["validation errors"]}), 400
        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)
        if not hero or not power:
            return jsonify({"errors": ["validation errors"]}), 400
        hp = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
        db.session.add(hp)
        db.session.commit()
        return jsonify(hp.to_dict()), 201

    return app
    
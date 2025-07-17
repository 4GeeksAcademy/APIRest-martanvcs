import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoritePlanet, FavoriteCharacter

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ---------- GET /people ----------
@app.route('/people', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    return jsonify([p.serialize() for p in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(person.serialize()), 200

# ---------- GET /planets ----------
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# ---------- GET /users ----------
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

# ---------- GET /users/favorites ----------
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    planet_favs = FavoritePlanet.query.filter_by(user_id=user.id).all()
    character_favs = FavoriteCharacter.query.filter_by(user_id=user.id).all()

    favorites = {
        "planets": [f.serialize() for f in planet_favs],
        "characters": [f.serialize() for f in character_favs]
    }
    return jsonify(favorites), 200

# ---------- POST /users/favorite/people ----------
@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(user_id, people_id):
    character = Character.query.get(people_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    existing = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=people_id).first()
    if existing:
        return jsonify({"message": "Character already in favorites"}), 200

    fav = FavoriteCharacter(user_id=user_id, character_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Character favorite added"}), 201

# ---------- POST /users/favorite/planet ----------
@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    existing = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing:
        return jsonify({"message": "Planet already in favorites"}), 200

    fav = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Planet favorite added"}), 201

# ---------- DELETE /users/favorite/people ----------
@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(user_id, people_id):
    fav = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=people_id).first()
    if not fav:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Character favorite removed"}), 200

# ---------- DELETE /users/favorite ----------
@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    fav = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Planet favorite removed"}), 200

# ---------- POST /people ----------
@app.route('/people', methods=['POST'])
def create_person():
    data = request.get_json()
    new_person = Character(
        name=data['name'],
        gender=data.get('gender'),
        birth_year=data.get('birth_year'),
        eye_color=data.get('eye_color')
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 201

# ---------- PUT /people ----------
@app.route('/people/<int:people_id>', methods=['PUT'])
def update_person(people_id):
    data = request.get_json()
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404

    person.name = data.get('name', person.name)
    person.gender = data.get('gender', person.gender)
    person.birth_year = data.get('birth_year', person.birth_year)
    person.eye_color = data.get('eye_color', person.eye_color)

    db.session.commit()
    return jsonify(person.serialize()), 200

# ---------- DELETE /people ----------
@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404

    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "Character deleted"}), 200

# ---------- POST /planets ----------
@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    new_planet = Planet(
        name=data['name'],
        climate=data.get('climate'),
        population=data.get('population'),
        terrain=data.get('terrain')
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

# ---------- PUT /planets ----------
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    data = request.get_json()
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    planet.name = data.get('name', planet.name)
    planet.climate = data.get('climate', planet.climate)
    planet.population = data.get('population', planet.population)
    planet.terrain = data.get('terrain', planet.terrain)

    db.session.commit()
    return jsonify(planet.serialize()), 200

# ---------- DELETE /planets ----------
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    db.session.delete(planet)
    db.session.commit()
    return jsonify({"message": "Planet deleted"}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

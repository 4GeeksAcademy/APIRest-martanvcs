import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

# Endpoints

# GET personajes


@app.route('/people', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    return jsonify([p.serialize() for p in people]), 200

# GET personaje por ID


@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(person.serialize()), 200

# GET planetas


@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200

# GET planeta por ID


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# GET usuarios


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

# GET favoritos del usuario


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = User.query.get(1)
    if not user:
        return jsonify({"error": "User not found"}), 404
    favorites = Favorite.query.filter_by(user_id=user.id).all()
    return jsonify([f.serialize() for f in favorites]), 200

# POST favorito (personaje)


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id):
    user_id = 1
    character = Character.query.get(people_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    fav = Favorite(user_id=user_id, character_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Character favorite added"}), 200

# POST favorito (planeta)


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Planet favorite added"}), 200

#  DEL favorito (personaje)


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(people_id):
    user_id = 1
    fav = Favorite.query.filter_by(
        user_id=user_id, character_id=people_id).first()
    if not fav:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Character favorite removed"}), 200

# DEL favorito (planeta)


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1
    fav = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Planet favorite removed"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

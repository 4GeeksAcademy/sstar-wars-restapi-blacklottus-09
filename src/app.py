"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite, People, Planet
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

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


@app.route('/people', methods=["GET"])
def get_people():
    all_people = People.query.all()
    if not all_people:
        return jsonify({"msg": "No people available"}), 404
    return jsonify([person.serialize() for person in all_people]), 200


@app.route('/people/<int:id>', methods=["GET"])
def get_person(id):
    person = People.query.get(id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404
    return jsonify(person.serialize()), 200


@app.route('/planets', methods=["GET"])
def get_planets():
    all_planets = Planet.query.all()
    if not all_planets:
        return jsonify({"msg": "No planets available"}), 404
    return jsonify([planet.serialize() for planet in all_planets]), 200


@app.route('/planets/<int:id>', methods=["GET"])
def get_planet(id):
    planet = Planet.query.get(id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200


@app.route('/users', methods=["GET"])
def get_users():
    all_users = User.query.all()

    if not all_users:
        return jsonify({"msg": "No users available"}), 404

    return jsonify([user.serialize() for user in all_users]), 200


@app.route('/users/favorites', methods=["GET"])
def get_favorites():
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"msg": "User not found"}), 404

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    if not favorites:
        return jsonify({"msg": "No favorites available"}), 404
    return jsonify([favorite.serialize() for favorite in favorites]), 200


@app.route('/favorite/planet/<int:planet_id>', methods=["POST"])
def add_favorite_planet(planet_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"msg": "user_id is required in the request body"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, favorite_type='planet', favorite_id=planet_id).first()
    if existing_favorite:
        return jsonify({"msg": "Planet is already in favorites"}), 400
    new_favorite = Favorite(
        user_id=user_id, favorite_type='planet', favorite_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet added successfully"}), 201


@app.route('/favorite/people/<int:people_id>', methods=["POST"])
def add_favorite_person(people_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"msg": "user_id is required in the request body"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404
    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, favorite_type='people', favorite_id=people_id).first()
    if existing_favorite:
        return jsonify({"msg": "Person is already in favorites"}), 400
    new_favorite = Favorite(
        user_id=user_id, favorite_type='people', favorite_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite person added successfully"}), 201


@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"msg": "user_id is required in the request body"}), 400
    favorite = Favorite.query.filter_by(
        user_id=user_id, favorite_type='planet', favorite_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted successfully"}), 200


@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_person(people_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"msg": "user_id is required in the request body"}), 400
    favorite = Favorite.query.filter_by(
        user_id=user_id, favorite_type='people', favorite_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite person deleted successfully"}), 200

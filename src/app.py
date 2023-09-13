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
from models import db, User,  Planets, Characters, Starships, Favorites
#from models import Person

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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():
    user_query = User.query.all()
    results = list(map(lambda item: item.serialize(), user_query))
    print(results)
    if results == []:
        return jsonify({"msg": "There are no users"}), 404

    response_body = {
        "msg": "These are the users",
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    one_user_query = User.query.filter_by(id=user_id).first()
    if one_user_query is None:
         return jsonify({"msg": "Username does not exist"}), 404

    response_body = {
        "msg": "User",
        "user_name": one_user_query.serialize()
    }

    return jsonify(response_body), 200

@app.route('/favorites', methods=['GET'])
def get_favorites():
    get_favorites_query = Favorites.query.all()
    results = list(map(lambda item: item.serialize(),get_favorites_query))
    print(results)
    if results == []:
         return jsonify({"msg":"There are no favorites"}), 404

    response_body = {
        "msg": "These users added favorites",
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/favorites/<int:favorites_id>', methods=['GET'])
def favorites(favorites_id):
    favorites_query = Favorites.query.filter_by(id= favorites_id).first()
    print(favorites_query)
    if favorites_query is None:
         return jsonify({"msg":"The list is empty"}), 404

    response_body = {
        "msg": "These are your favorites",
        "result": favorites_query.serialize()
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    characters_query = Characters.query.all()
    results = list(map(lambda item: item.serialize(),characters_query))
    print(results)
    if results == []:
         return jsonify({"msg":"There are no characters"}), 404

    response_body = {
        "msg": "These are the characters",
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def character(character_id):
    print(character_id)
    character_query = Characters.query.filter_by(id= character_id).first()
    print(character_query)
    if character_query is None:
         return jsonify({"msg":"The character does not exist"}), 404

    response_body = {
        "msg": "Character",
        "result": character_query.serialize()
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets_query = Planets.query.all()
    results = list(map(lambda item: item.serialize(),planets_query))
    print(results)
    if results == []:
         return jsonify({"msg":"There are no planets"}), 404

    response_body = {
        "msg": "These are the planets",
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def planet(planet_id):
    print(planet_id)
    planet_query = Planets.query.filter_by(id= planet_id).first()
    print(planet_query)
    if planet_query is None:
         return jsonify({"msg":"The planet does not exist"}), 404

    response_body = {
        "msg": "Planet",
        "result": planet_query.serialize()
    }

    return jsonify(response_body), 200

@app.route('/starhips', methods=['GET'])
def get_starships():
    starhips_query = Starships.query.all()
    results = list(map(lambda item: item.serialize(), starhips_query))
    print(results)
    if results == []:
         return jsonify({"msg": "There are no starships"}), 404

    response_body = {
        "msg": "These are the starships",
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/starships/<int:starship_id>', methods=['GET'])
def starship(starship_id):
    print(starship_id)
    starship_query = Starships.query.filter_by(id= starship_id).first()
    print(starship_query)
    if starship_query is None:
         return jsonify({"msg": "The starship does not exist"}), 404

    response_body = {
        "msg": "Starship",
        "results": starship_query.serialize()
    }

    return jsonify(response_body), 200 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

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

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
with app.app_context():
    db.create_all()
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

# user methods

@app.route('/user', methods=['GET'])
def get_users():
    users= User.query.all()
    all_users = list(map(lambda item: item.serialize(), users))
    return jsonify(all_users), 200

@app.route('/user', methods=['POST'])
def new_user():
    request_body_user = request.get_json()
    another_user = User(username=request_body_user["username"], email=request_body_user["email"], password=request_body_user["password"])
    db.session.add(another_user)
    db.session.commit()
    return jsonify(request_body_user), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    request_body_user = request.get_json()
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    if "username" in request_body_user:
        user1.username = request_body_user["username"]
    if "password" in request_body_user:
        user1.password = request_body_user["password"]
    if "email" in request_body_user:
        user1.email = request_body_user["email"]
    db.session.commit()
    return jsonify(request_body_user), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()
    return jsonify("User successfully deleted"), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    one_user_query = User.query.filter_by(id=user_id).first()
    if one_user_query is None:
         raise APIException('User does not exist', status_code=404)
    return jsonify(one_user_query.serialize()), 200

# favorites methods

@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    user = get_one_user()
    if not user:
        raise APIException('User not found', status_code=404)
    user_favorites = Favorites.query.filter_by(user_id=user.id).all()
    if not user_favorites:
        raise APIException('User has no favorites', status_code=404)
    serialized_favorites = [favorite.serialize() for favorite in user_favorites]
    return jsonify(serialized_favorites), 200


#@app.route('/favorites/characters/<int:character_id>', methods=['POST'])
#def add_character_favorite(character_id):
    


# characters methods

@app.route('/characters', methods=['GET'])
def get_characters():
    characters_query = Characters.query.all()
    results = list(map(lambda item: item.serialize(),characters_query))
    if results == []:
         raise APIException('There are no characters', status_code=404)
    return jsonify(results), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def character(character_id):
    character_query = Characters.query.filter_by(id= character_id).first()
    if character_query is None:
         raise APIException('The character does not exist', status_code=404)
    return jsonify(character_query), 200

# planets methods

@app.route('/planets', methods=['GET'])
def get_planets():
    planets_query = Planets.query.all()
    results = list(map(lambda item: item.serialize(),planets_query))
    if results == []:
         raise APIException('There are no planets', status_code=404)
    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def planet(planet_id):
    planet_query = Planets.query.filter_by(id= planet_id).first()
    if planet_query is None:
         raise APIException('The planet does not exist', status_code=404)
    return jsonify(planet_query), 200

# starships methods

@app.route('/starhips', methods=['GET'])
def get_starships():
    starhips_query = Starships.query.all()
    results = list(map(lambda item: item.serialize(), starhips_query))
    if results == []:
         raise APIException('There are no starships', status_code=404)
    return jsonify(results), 200

@app.route('/starships/<int:starship_id>', methods=['GET'])
def starship(starship_id):
    starship_query = Starships.query.filter_by(id= starship_id).first()
    if starship_query is None:
        raise APIException('The starship does not exist', status_code=404)
    return jsonify(starship_query), 200 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

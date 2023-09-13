from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True, default=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    starship_id = db.Column(db.Integer, db.ForeignKey('starships.id'), nullable=True)
    user = db.relationship('User', backref='favorites')
    character = db.relationship('Characters', backref='favorites')
    planet = db.relationship('Planets', backref='favorites')
    starship = db.relationship('Starships', backref='favorites')
 
    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id_favorito": self.id,
            "usuario": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "starship_id": self.starship_id        
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    height = db.Column(db.String(50), unique=False, nullable=False)
    mass = db.Column(db.String(50), unique=False, nullable=False)
    hair_color = db.Column(db.String(50), unique=False, nullable=False)
    skin_color = db.Column(db.String(50), unique=False, nullable=False)
    eye_color = db.Column(db.String(50), unique=False, nullable=False)
    birth_year = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.String(50), unique=False, nullable=False)
    
    
    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin-color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    diameter = db.Column(db.String(50), unique=False, nullable=False)
    rotation_period = db.Column(db.String(50), unique=False, nullable=False)
    orbital_period = db.Column(db.String(50), unique=False, nullable=False)
    gravity = db.Column(db.String(50), unique=False, nullable=False)
    population = db.Column(db.String(50), unique=False, nullable=False)
    climate = db.Column(db.String(50), unique=False, nullable=False)
    terrain = db.Column(db.String(50), unique=False, nullable=False)
    surface_water = db.Column(db.String(50), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
        }                 

class Starships(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    model = db.Column(db.String(50), unique=False, nullable=False)
    starship_class = db.Column(db.String(50), unique=False, nullable=False)
    manufacturer = db.Column(db.String(50), unique=False, nullable=False)
    cost_in_credits = db.Column(db.String(50), unique=False, nullable=False)
    length = db.Column(db.String(50), unique=False, nullable=False)
    crew = db.Column(db.String(50), unique=False, nullable=False)
    passengers = db.Column(db.String(50), unique=False, nullable=False)
    max_atmosphering_speed = db.Column(db.String(50), unique=False, nullable=False)
    hyperdrive_rating = db.Column(db.String(50), unique=False, nullable=False)
    MGLT = db.Column(db.String(50), unique=False, nullable=False)
    cargo_capacity = db.Column(db.String(50), unique=False, nullable=False)
    consumables = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<Starships %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "starship_class": self.starship_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew, 
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "hyperdrive_ratin": self.hyperdrive_rating,
            "MGLT": self.MGLT,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables
        }
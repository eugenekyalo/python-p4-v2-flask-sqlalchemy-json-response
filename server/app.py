#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from models import db, Pet

print("Initializing Flask app...")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

print("Setting up database...")

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    print("Accessing index route")
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    print(f"Accessing pet_by_id route with id: {id}")
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        body = {'id': pet.id,
                'name': pet.name,
                'species': pet.species}
        status = 200
    else:
        body = {'message': f'Pet {id} not found.'}
        status = 404

    return make_response(body, status)

@app.route('/species/<string:species>')
def pet_by_species(species):
    print(f"Accessing pet_by_species route with species: {species}")
    pets = []
    for pet in Pet.query.filter(Pet.species.ilike(f'%{species}%')).all():
        pet_dict = {'id': pet.id,
                    'name': pet.name,
                    'species': pet.species
                    }
        pets.append(pet_dict)
    
    if pets:
        body = {'count': len(pets),
                'pets': pets
                }
        status = 200
    else:
        body = {'message': f'No pets found for species "{species}".'}
        status = 404

    return make_response(body, status)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(port=5555, debug=True)

print("This line should not be reached if the app is running correctly.")
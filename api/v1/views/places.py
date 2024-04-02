#!/usr/bin/python3
"""
creating a view for Place objects
"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    '''RETRIEVE THE LIST OF ALL CITY OBJECTS'''
    city = storage.get(City, city_id)
    if city:
        cities_lst = [obj.to_dict() for obj in city.places]
    else:
        abort(404)
    return jsonify(cities_lst)


@app_views.route('/places/<string:place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    '''retrive a place object by its id'''
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''delete a place object'''
    place = storage.get(Place, place_id)
    if place:
        place.delete()
    else:
        abort(404)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''create a place object'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    state_data = request.get_json()
    place = Place(**state_data)
    place.city_id = city.id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(city_id):
    '''update a place by its id'''
    place = storage.get(Place, city_id)
    data = request.get_json()
    if not request.get_json():
        abort(400, 'Not a JSON')
    if place:
        for key, value in data.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(place, key, value)
    else:
        abort(404)
    storage.save()
    return jsonify(place.to_dict()), 200

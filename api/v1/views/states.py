#!/usr/bin/python3
"""
creating a view for State objects
"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    '''RETRIEVE THE LIST OF ALL State OBJECTS'''
    obj_lst = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(obj_lst)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state(state_id):
    '''retrive a state object by its id'''
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    '''delete a state object'''
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    '''create a state object'''
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    user_data = request.get_json()
    state = State(**user_data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    '''update a state by its id'''
    state = storage.get(State, state_id)
    data = request.get_json()
    if not request.json:
        abort(400, 'Not a JSON')
    if state:
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
    else:
        abort(404)
    storage.save()
    return jsonify(state.to_dict()), 200

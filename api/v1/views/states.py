#!/usr/bin/python3
'''state view'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def all_states():
    '''Return all the states in the storage'''
    instances = storage.all(State)
    states_list = []
    for instance in instances.values():
        states_list.append(instance.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def search_by_id(state_id=None):
    '''Filter state by id'''
    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_obj(state_id=None):
    '''Delete state of the provided id'''
    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        # Return an empty dictionary with status code 200
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    '''Create a new state'''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        # method extracts and parses data from request body
        # if data is in json format, it return python dict or list
        # If the data is not valid JSON, raise an error or return None
        if 'name' not in data:
            abort(400, description='Missing name')
        new_state = State(**data)
        # Create a new instance of state and pass the key value pairs
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id=None):
    '''Update state of provided id'''
    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    else:
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(object, key, value)
        storage.save()
        return jsonify(object.to_dict()), 200

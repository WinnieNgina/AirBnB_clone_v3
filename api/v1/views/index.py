#!/usr/bin/python3
'''Index file'''
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status_check():
    '''Returns status code'''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_items():
    objects = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
        }
    return jsonify(objects)

#!/usr/bin/python3
"""Defines app main index"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route("/status")
def get_status():
    """Returns a JSON: "status": "OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def get_stats():
    """retrieves the number of each objects by type"""
    classes = {"amenities": Amenity,
               "cities": City,
               "places": Place,
               "reviews": Review,
               "states": State,
               "users": User}
    stats_dict = dict()

    for k, v in classes.items():
        stats_dict[k] = storage.count(v)
    return jsonify(stats_dict)

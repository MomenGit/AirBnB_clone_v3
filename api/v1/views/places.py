#!/usr/bin/python3
"""Defines app main index"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.all(City).get("City.{}".format(city_id))
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """Retrieves an Place object using its id"""
    place = storage.all(Place).get("{}.{}".format(Place.__name__, place_id))
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Creates an Place object"""
    city = storage.all(City).get("{}.{}".format(City.__name__, city_id))
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    user = storage.all(User).get(
        "{}.{}".format(User.__name__, data.get("user_id")))
    if user is None:
        abort(404)
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Update an Place object using its id"""
    place = storage.all(Place).get("{}.{}".format(Place.__name__, place_id))
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes an Place object using its id"""
    place = storage.all(Place).get("{}.{}".format(Place.__name__, place_id))
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200

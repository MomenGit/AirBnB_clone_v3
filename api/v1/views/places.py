#!/usr/bin/python3
"""Defines app main index"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


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


@app_views.route("/cities/<city_id>/places", methods=["POST"])
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
    user = storage.all(User).get(
        "{}.{}".format(User.__name__, data.get("user_id")))
    if user is None:
        abort(404)
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    data["city_id"] = city_id
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
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
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


@app_views.route("/places_search", methods=["POST"])
def places_search():
    """
    retrieves all Place objects
    depending of the JSON in the body of the request.
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    states_data = data.get('states', [])
    cities_data = data.get('cities', [])
    amenities_data = data.get('amenities', [])
    if (len(data) == 0 and len(states_data) == 0 and
            len(cities_data) == 0 and len(amenities_data) == 0):
        all_places = storage.all(Place).values()
        places_list = list()
        for place in all_places:
            places_list.append(place.to_dict())
        return (jsonify(places_list))

    cities_list = list()
    places_list = list()
    amenities_list = list()
    # add cities in states to cities list
    if len(states_data) != 0:
        for state_id in states_data:
            state = storage.get(State, state_id)
            if state:
                cities_list.extend(state.cities)
    if len(cities_data) != 0:
        for city_id in cities_data:
            city = storage.get(City, city_id)
            if city:
                cities_list.append(city)

    # Add places in cities to places list
    for city in cities_list:
        places_list.extend(city.places)

    # get ameniteies
    if len(amenities_data) != 0:
        for amenity_id in amenities_data:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities_list.append(amenity)

    # get places that have all amenities
    result = list()
    for amenity in amenities_list:
        for place in places_list:
            if amenity not in place.amenities:
                places_list.remove(place)
    result = [place.to_dict() for place in places_list]
    return (jsonify(result))

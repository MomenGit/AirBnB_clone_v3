#!/usr/bin/python3
"""Defines app main index"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def get_place_amenities(place_id):
    """Retrieves the list of all Review objects"""
    place = storage.all(Place).get("{}.{}".format(Place.__name__, place_id))
    if place is None:
        abort(404)

    place_amenities = []
    if storage_t == "db":
        place_amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = storage.all(Amenity)
        for id in place.amenity_ids:
            amenity = amenities.get("{}.{}".format(Amenity.__name__, id))
            if amenity is not None:
                place_amenities.append(amenity.to_dict())

    return jsonify(place_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def link_place_amenity(place_id, amenity_id):
    """Link a Place object with an Amenity Object"""
    place = storage.all(Place).get(
        "{}.{}".format(Place.__name__, place_id))
    if place is None:
        abort(404)
    amenity = storage.all(Amenity).get(
        "{}.{}".format(Amenity.__name__, amenity_id))
    if Amenity is None:
        abort(404)
    if storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity.id)

    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/place/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    """Deletes a link between an Amenity object and a Place object"""
    place = storage.all(Place).get(
        "{}.{}".format(Place.__name__, place_id))
    if place is None:
        abort(404)
    amenity = storage.all(Amenity).get(
        "{}.{}".format(Amenity.__name__, amenity_id))
    if Amenity is None:
        abort(404)
    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        else:
            place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        else:
            place.amenity_ids.remove(amenity.id)

    storage.save()
    return jsonify({}), 200

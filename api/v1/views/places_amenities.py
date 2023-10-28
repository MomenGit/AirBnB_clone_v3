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
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place_amenities = [amenity.to_dict() for amenity in place.amenities]

    return jsonify(place_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def link_place_amenity(place_id, amenity_id):
    """Link a Place object with an Amenity Object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if Amenity is None:
        abort(404)
    linked = False
    if storage_t == "db":
        linked = amenity in place.amenities
        if not linked:
            place.amenities.append(amenity)
    else:
        linked = amenity_id in place.amenity_ids
        if not linked:
            place.amenity_ids.append(amenity_id)

    if linked:
        return jsonify(amenity.to_dict()), 200

    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    """Deletes a link between an Amenity object and a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if Amenity is None:
        abort(404)
    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        else:
            place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        else:
            place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200

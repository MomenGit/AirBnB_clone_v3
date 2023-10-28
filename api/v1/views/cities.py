#!/usr/bin/python3
"""Defines app main index"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<string:state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def get_list_city(state_id):
      """Retrieves the list of all objects"""
      obj = storage.get(State, state_id)
      if obj is None:
          abort(404)
      all_objs = obj.cities
      objs_list = list()
      for obj in all_objs:
          objs_list.append(obj.to_dict())
      return jsonify(objs_list)


@app_views.route("/states/<string:state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def create_new_city(state_id):
    """Create a new object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    if "name" not in json_data:
        abort(400, description="Missing name")

    json_data["state_id"] = state_id
    obj = City(**json_data)
    obj.save()

    response = make_response(jsonify(obj.to_dict()))
    response.status_code = 201
    return response


@app_views.route("/cities/<city_id>",
                 methods=['GET'], strict_slashes=False)
def get_obj_city(city_id):
    """Retrieves an object using id"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_obj_city(city_id):
    """Delete an object using id"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()
    response = make_response(jsonify({}))
    response.status_code = 200
    return response


@app_views.route("/cities/<city_id>",
                 methods=['PUT'], strict_slashes=False)
def edit_obj_city(city_id):
    """Update an object using id"""
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")

    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    for key, value in json_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()

    response = make_response(jsonify(obj.to_dict()))
    response.status_code = 200
    return response

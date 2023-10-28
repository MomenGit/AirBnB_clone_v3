#!/usr/bin/python3
"""Defines app main index"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.user import User
from models import storage

cls = User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_list_user():
    """Retrieves the list of all objects"""
        all_objs = storage.all(cls).values()
        objs_list = list()

        for obj in all_objs:
            objs_list.append(obj.to_dict())
        return jsonify(objs_list)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_new_user():
    """Create a new object"""
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    if "email" not in json_data:
        abort(400, description="Missing email")
    if "password" not in json_data:
        abort(400, description="Missing password")

    obj = cls(**json_data)
    obj.save()

    response = make_response(jsonify(obj.to_dict()))
    response.status_code = 201
    return response


@app_views.route("/users/<user_id>",
                 methods=['GET'], strict_slashes=False)
def get_obj_user(user_id):
    """Retrieves an object using id"""
    obj = storage.get(cls, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/users/<user_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_obj_user(user_id):
    """Delete an object using id"""
    obj = storage.get(cls, user_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()
    response = make_response(jsonify({}))
    response.status_code = 200
    return response


@app_views.route("/users/<user_id>",
                 methods=['PUT'], strict_slashes=False)
def edit_obj_user(user_id):
    """Update an object using id"""
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")

    obj = storage.get(cls, user_id)
    if obj is None:
        abort(404)

    for key, value in json_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()

    response = make_response(jsonify(obj.to_dict()))
    response.status_code = 200
    return response

#!/usr/bin/python3
"""Defines app main index"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def get_status():
    """Returns a JSON: "status": "OK"""
    return jsonify({"status": "OK"})

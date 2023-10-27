#!/usr/bin/python3
"""Defines app_views flask blueprint for views package"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from .index import *

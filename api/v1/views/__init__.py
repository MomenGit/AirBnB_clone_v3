#!/usr/bin/python3
"""Defines app_views flask blueprint for views package"""
from flask import Blueprint

from .index import *
from .states import *
from .cities import *
from .amenities import *
from .users import *
from .places import *
from .places_reviews import *
from .places_amenities import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

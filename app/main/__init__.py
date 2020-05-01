from flask import Blueprint

admin = Blueprint("main", __name__)

from . import views


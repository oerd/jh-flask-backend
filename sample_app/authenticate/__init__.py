from flask import Blueprint

bp = Blueprint('authenticate', __name__)

from .views import get_all, add  # noqa

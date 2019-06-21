from flask import Blueprint

bp = Blueprint('users', __name__)

from .views import get_all, add  # noqa

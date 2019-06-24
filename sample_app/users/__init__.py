from flask import Blueprint

users_bp = Blueprint('users', __name__)

from .views import get_all, add  # noqa

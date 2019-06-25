from flask import Blueprint

authentication_bp = Blueprint('auth', __name__)

from .views import authenticate  # noqa

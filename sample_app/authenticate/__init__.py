from flask import Blueprint

authentication_bp = Blueprint('authentication', __name__)

from .views import authenticate # noqa

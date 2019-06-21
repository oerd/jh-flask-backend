from flask import request, jsonify, current_app
from werkzeug.exceptions import NotAcceptable, InternalServerError, BadRequest
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from . import bp
from utils.web import request_wants_json


@bp.route('')
def authenticate():
    """Authenticate a user."""
    if not request_wants_json():
        raise NotAcceptable()
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify({
            "type": "https://www.jhipster.tech/problem/problem-with-message",
            "title": "Unauthorized",
            "status": 401,
            "detail": "Bad credentials",
            "path": "/api/authenticate",
            "message": "error.http.401"
        })
    if username == 'user' and password == 'user':
        identity = {'sub': username, 'auth': 'ROLE_USER', "exp": 1563635440}
        access_token = create_access_token(identity=identity)



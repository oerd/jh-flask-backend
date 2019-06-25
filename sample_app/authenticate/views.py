from flask import request, jsonify
from werkzeug.exceptions import NotAcceptable
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from . import authentication_bp as auth_bp
from utils.web import request_wants_json


@auth_bp.route('/authenticate', methods=['POST'])
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
        return jsonify(access_token=access_token), 200


@auth_bp.route('/account')
def get_account():
    current_user = get_jwt_identity()
    print("Current user jwt identity:", current_user)
    user = {
        'id': 4,
        'login': "user",
        'firstName': "User",
        'lastName': "User",
        'email': "user@localhost",
        'imageUrl': "",
        'activated': True,
        'langKey': "en",
        'createdBy': "system",
        'createdDate': None,
        'lastModifiedBy': "system",
        'lastModifiedDate': None,
        'authorities': ["ROLE_USER"]
    }
    return jsonify(user), 200

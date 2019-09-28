from flask import request, jsonify
from werkzeug.exceptions import NotAcceptable
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from . import authentication_bp as auth_bp
from utils.web import request_wants_json
from ..users.models import User


bad_creds = {
            "type": "https://www.jhipster.tech/problem/problem-with-message",
            "title": "Unauthorized",
            "status": 401,
            "detail": "Bad credentials",
            "path": "/api/authenticate",
            "message": "error.http.401"
        }

unauthorized = {
              "type": "https://www.jhipster.tech/problem/problem-with-message",
              "title": "Unauthorized",
              "status": 401,
              "detail": "Full authentication is required to access this resource",
              "path": "/api/account",
              "message": "error.http.401"
            }

@auth_bp.route('/authenticate', methods=['POST'])
def authenticate():
    """Authenticate a user."""
    if not request_wants_json():
        raise NotAcceptable()
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    print("AUTH for: {}/{}".format(username, password))

    if not username or not password:
        return jsonify(bad_creds)

    user = User.query.filter_by(login=username).first()
    print("AUTH got user: {}".format(user))

    if user.check_password(password):
        print("AUTH check password hash ok")
        access_token = create_access_token(identity={
            'sub': user.login,
            'auth': [a.name for a in user.authorities],
            'exp': 1563635440
        })
        return jsonify(access_token=access_token), 200

    return jsonify(bad_creds), 401


@auth_bp.route('/register', methods=['POST'])
def register_user():
    """Register a new user."""
    if not request_wants_json():
        raise NotAcceptable()
    data = request.get_json()
    print(data)
    lang_key = data.get('langKey', 'en')
    u = User(data.get('login'), data.get('password'), "", "", data.get('email'), lang_key=lang_key)
    u.save()
    return '', 201


@auth_bp.route('/account')
@jwt_required
def get_account():
    current_user = get_jwt_identity()
    print("Current user jwt identity:", current_user)

    if not current_user:
        return jsonify(unauthorized), 401

    return jsonify(current_user), 200

from flask import request, jsonify, current_app
from werkzeug.exceptions import NotAcceptable, InternalServerError, BadRequest
from utils.web import request_wants_json

from . import users_bp as bp
from .models import User
from .schema import UserSchema


@bp.route('')
def get_all():
    """Return all users."""
    if not request_wants_json():
        raise NotAcceptable()

    items = User.query.all()
    return jsonify(UserSchema(many=True).dump(items).data)


@bp.route('', methods=['POST'])
def add():
    if not request.is_json:
        raise NotAcceptable()

    user, errors = UserSchema().load(request.json)
    if errors:
        raise BadRequest()

    try:
        user.save()
    except Exception as e:
        current_app.logger.warning(e, exc_info=True)
        raise InternalServerError()

    return "", 200


@bp.route('/<int:user_id>')
def get_one(user_id):
    if not request_wants_json():
        raise NotAcceptable()

    user = User.query.get_or_404(user_id)
    return jsonify(UserSchema().dump(user).data)


@bp.route('/login', methods=['PUT'])
def update_one(login):
    if not request_wants_json() or not request.is_json:
        raise NotAcceptable()

    user = User.query.get_or_404(login)

    errors = UserSchema().validate(request.json)
    if errors:
        raise BadRequest()

    try:
        user.update(**request.json)
    except Exception as e:
        current_app.logger.warning(e, exc_info=True)
        raise InternalServerError()
    return jsonify(UserSchema(only=('name', 'address', 'city', 'owm_id')).dump(user).data)


@bp.route('/login', methods=['DELETE'])
def delete(login):
    user = User.query.get_or_404(login)
    try:
        user.delete()
    except Exception as e:
        current_app.logger.warning(e, exc_info=True)
        raise InternalServerError
    return "", 200

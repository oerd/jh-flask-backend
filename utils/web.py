from pprint import pprint

from flask import request

import logging

from flask.views import MethodView
from marshmallow import ValidationError
from werkzeug.exceptions import InternalServerError

logger = logging.getLogger('sample_app')


# TODO: this might be superfluous, our API provides json, independently of HTTP request Content-Type
def request_wants_json(ignore_rest=True):
    best = request.accept_mimetypes .best_match(['application/json', 'text/html'])
    if ignore_rest:
        return best == 'application/json'
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']


class BaseApi(MethodView):
    """ Example of a class inheriting from flask.views.MethodView

    All 3 request methods are available at /api/example
    """
    def __init__(self, **kwargs):
        super(BaseApi, self).__init__(**kwargs)

    def get(self):
        """ getAllEntities() """
        result = self.Model.query.all()
        return self.Schema(many=True).jsonify(result), 200

    def post(self):
        """ createEntity() """
        try:
            item = self.Schema().load(request.json)
        except ValidationError as err:
            pprint(err.messages)
            raise InternalServerError
        else:
            item.save()
            return self.Schema().jsonify(item), 200

    def put(self, entity):
        """ updateEntity() """
        return "Responding to a PUT request"


class BaseItemsApi(MethodView):
    """ Base class to handle item APIs

     treat `/api/entity/<int:entity_id>`-style URLs """
    def __init__(self, **kwargs):
        super(BaseItemsApi, self).__init__(**kwargs)

    def get(self, entity):
        """ getEntity() """
        result = self.Model.query.get_or_404(entity)
        return self.schema.jsonify(result), 200

    def delete(self, entity):
        """ deleteEntity() """
        result = self.Model.query.get_or_404(entity)
        if result.delete():
            return "", 200
        raise InternalServerError
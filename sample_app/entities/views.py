from flask import request
from flask.views import MethodView
from werkzeug.exceptions import InternalServerError
from marshmallow import ValidationError
from pprint import pprint

from .models import BankAccount, Operation, Label
from .schema import BankAccountSchema, OperationSchema, LabelSchema


# FIXME: Refactor this away!
class BankAccountsApi(MethodView):
    """ Example of a class inheriting from flask.views.MethodView

    All 5 request methods are available at /api/example/<entity>
    """
    schema = BankAccountSchema(many=True)

    def get(self):
        """ Responds to GET requests """
        result = BankAccount.query.all()
        return self.schema.jsonify(result), 200

    def post(self):
        """ Responds to POST requests """
        item = None
        pprint(request.json)
        try:
            item = BankAccountSchema().load(request.json)
        except ValidationError as err:
            pprint(item)
            pprint(err.messages)
        else:
            item.save()
        return self.schema.jsonify(item), 200

    def put(self):
        """ Responds to PUT requests """
        return "Responding to a PUT request"


class BankAccountItemsApi(MethodView):
    schema = BankAccountSchema()

    def get(self, entity):
        """ getBankAccount() """
        account = BankAccount.query.get_or_404(entity)
        return self.schema.jsonify(account), 200

    def delete(self, entity):
        """ deleteBankAccount """
        result = BankAccount.query.get_or_404(entity)
        if result.delete():
            return "", 200
        raise InternalServerError


class BaseApi(MethodView):
    """ Example of a class inheriting from flask.views.MethodView

    All 5 request methods are available at /api/example/<entity>
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


class LabelsApi(BaseApi):
    Model = Label
    Schema = LabelSchema


class LabelItemsApi(BaseApi):
    Model = Label
    Schema = LabelSchema


class OperationsApi(BaseApi):
    Model = Operation
    Schema = OperationSchema


class OperationItemsApi(BaseApi):
    Model = Operation
    Schema = OperationSchema

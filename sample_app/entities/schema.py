from sample_app import ma
from marshmallow import post_load

from .models import BankAccount, Operation, Label
from ..users.schema import UserSchema


class OperationSchema(ma.ModelSchema):
    class Meta:
        model = Operation


class LabelSchema(ma.ModelSchema):
    class Meta:
        model = Label
        # FIXME: make `id` read-only, schema -> ValueType object
        fields = ('id', 'label', '_links')

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {"self": ma.URLFor("label_items_api", entity="<id>"), "collection": ma.URLFor("labels_api")}
    )


class BankAccountSchema(ma.ModelSchema):
    class Meta:
        model = BankAccount
        fields = ('balance', 'id', 'name', 'operations', 'user', '_links')

    user = ma.Nested(UserSchema)
    operations = ma.List(ma.Nested(OperationSchema))

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {"self": ma.URLFor("account_items_api", entity="<id>"), "collection": ma.URLFor("accounts_api")}
    )

    @post_load
    def make_account(self, data, **kwargs):
        return BankAccount(**data)

from utils.web import BaseApi, BaseItemsApi
from .models import BankAccount, Operation, Label
from .schema import BankAccountSchema, OperationSchema, LabelSchema


class BankAccountsApi(BaseApi):
    Model = BankAccount
    Schema = BankAccountSchema


class BankAccountItemsApi(BaseItemsApi):
    Model = BankAccount
    Schema = BankAccountSchema


class LabelsApi(BaseApi):
    Model = Label
    Schema = LabelSchema


class LabelItemsApi(BaseItemsApi):
    Model = Label
    Schema = LabelSchema


class OperationsApi(BaseApi):
    Model = Operation
    Schema = OperationSchema


class OperationItemsApi(BaseItemsApi):
    Model = Operation
    Schema = OperationSchema

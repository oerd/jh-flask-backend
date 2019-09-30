from sample_app import db
from utils.data import Model

from ..users.models import User


class BankAccount(Model):
    __tablename__ = 'jhi_bank_account'

    name = db.Column(db.String)
    balance = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('jhi_user.id'))

    user = db.relationship('User', backref=db.backref('accounts', lazy='dynamic'))


class Label(Model):
    __tablename__ = 'jhi_label'

    label = db.Column(db.String)


operation_label_table = db.Table(
    "jhi_operation_label",
    db.Column("operation_id", db.Integer, db.ForeignKey('jhi_operation.id'), nullable=False),
    db.Column("label_id", db.Integer, db.ForeignKey('jhi_label.id'), nullable=False),
    db.PrimaryKeyConstraint('operation_id', 'label_id'))


class Operation(Model):
    __tablename__ = "jhi_operation"

    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String)
    amount = db.Column(db.Float, nullable=False)
    bank_account_id = db.Column(db.Integer, db.ForeignKey('jhi_bank_account.id'))

    bank_account = db.relationship('BankAccount', backref=db.backref('operations', lazy='dynamic'))
    labels = db.relationship('Label', secondary=operation_label_table, backref=db.backref('operations', lazy='dynamic'))

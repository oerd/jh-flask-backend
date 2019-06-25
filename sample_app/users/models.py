import datetime

from sample_app import db, bc
from utils.data import Model


user_authority_table = db.Table("jhi_user_authority",
                                db.Column("user_id", db.BigInteger, db.ForeignKey('jhi_user.id'), nullable=False),
                                db.Column("authority_name", db.String(50), db.ForeignKey('jhi_authority.name'), nullable=False),
                                db.PrimaryKeyConstraint('user_id', 'authority_name'))


class User(Model):
    __tablename__ = 'jhi_user'

    uid = db.Column(db.BigInteger, key="id", primary_key=True)
    login = db.Column("login", db.String(50), unique=True, nullable=False)  # TODO: have a validator regex for login!
    password = db.Column("password_hash", db.String(60))
    first_name = db.Column("first_name", db.String(50))
    last_name = db.Column("last_name", db.String(50))
    email = db.Column("email", db.String(191))
    image_url = db.Column("image_url", db.String(256))
    activated = db.Column("activated", db.Boolean)
    lang_key = db.Column("lang_key", db.String(10))
    activation_key = db.Column("activation_key", db.String(20))
    reset_key = db.Column("reset_key", db.String(20))
    created_by = db.Column("created_by", db.String(50))
    created_date = db.Column("created_date", db.DateTime)
    reset_date = db.Column("reset_date", db.DateTime)
    last_modified_by = db.Column("last_modified_by", db.String(50))
    last_modified_date = db.Column("last_modified_date", db.DateTime)

    authorities = db.relationship('UserAuthority', secondary=user_authority_table, backref="users")

    def __init__(self, login, password, first_name, last_name, email, activated=True, lang_key="en-US"):
        self.login = login
        self.password = bc.generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.activated = activated
        self.lang_key = lang_key
        self.created_date = datetime.datetime.now()

    def check_password(self, password_hash):
        return bc.check_password_hash(self.password, password_hash)


class UserAuthority(Model):
    __tablename__ = 'jhi_authority'

    name = db.Column("name", db.String(50), primary_key=True)

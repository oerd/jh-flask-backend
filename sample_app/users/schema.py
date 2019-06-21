from marshmallow import post_load

from sample_app import ma     # flask-marshmallow
from .models import User, UserAuthority  # SQLAlchemy model


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        strict = True
        only = ('login', 'password', 'first_name', 'last_name', 'email', 'activated', 'lang_key')

    @post_load
    def make_place(self, data):
        return User()


class UserAuthoritySchema(ma.ModelSchema):
    class Meta:
        model = UserAuthority
        strict = True
        only = ('name',)

    @post_load
    def make_place(self, data):
        return User()
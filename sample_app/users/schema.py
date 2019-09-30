from marshmallow import post_load

from sample_app import ma     # flask-marshmallow
from .models import User, UserAuthority  # SQLAlchemy model


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        strict = True
        only = ('login', 'password', 'first_name', 'last_name', 'email', 'activated', 'lang_key', '_links')

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {"self": ma.URLFor("users.get_one", user_id="<uid>"), "collection": ma.URLFor("users.get_all")}
    )

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class UserAuthoritySchema(ma.ModelSchema):
    class Meta:
        model = UserAuthority
        strict = True
        only = ('name',)

    @post_load
    def make_user_authority(self, data, **kwargs):
        return UserAuthority(**data)

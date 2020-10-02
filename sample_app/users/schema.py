from marshmallow import pre_load, post_load

from sample_app import ma                # flask-marshmallow
from utils.schema import JavaScriptMixin
from .models import User, UserAuthority  # SQLAlchemy model


class UserSchema(ma.SQLAlchemyAutoSchema, JavaScriptMixin):
    class Meta:
        model = User
        strict = True
        only = ('login', 'password', 'first_name', 'last_name', 'email', 'activated', 'lang_key', '_links')

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {"self": ma.URLFor("users.get_one", user_id="<uid>"), "collection": ma.URLFor("users.get_all")}
    )


class UserAuthoritySchema(ma.SQLAlchemyAutoSchema, JavaScriptMixin):
    class Meta:
        model = UserAuthority
        strict = True
        only = ('name',)

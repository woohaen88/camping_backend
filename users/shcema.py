from ninja import Schema, ModelSchema
from django.contrib.auth import get_user_model


class Signin(Schema):
    email: str
    password: str


class Signup(Signin):
    username: str | None
    password_confirm: str


class ChangePassword(Schema):
    old_password: str
    new_password: str
    new_password_confirm: str


class TinyUserSchema(ModelSchema):
    class Config:
        model = get_user_model()
        model_fields = [
            "id",
            "email",
            "username",
            "avatar",
            "first_name",
            "last_name",
        ]

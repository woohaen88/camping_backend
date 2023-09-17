from ninja import Schema


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

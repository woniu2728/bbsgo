from ninja import Schema


class LoginIn(Schema):
    username: str
    password: str


class TokenOut(Schema):
    token: str
    token_type: str = "bearer"


class AuthManifestOut(Schema):
    token_type: str
    header: str

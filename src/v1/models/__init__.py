from flask_restplus import fields
from typing import List, Optional
from .. import API_V1


class AuthToken:
    __model__ = API_V1.model('AuthToken', {
        'access_token': fields.String(readonly=True, description='The access token, contains the claims.'),
        'refresh_token': fields.String(readonly=True,
                                       description='The refresh token. Does not contain any information')
    })

    def __init__(self, access_token: str, refresh_token: str, /) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token


class Brand:
    __model__ = API_V1.model('Brand', {
        'id': fields.Integer(readonly=True, min=1, description='The brand id'),
        'name': fields.String(required=True, description='The brand name')
    })

    def __init__(self, identifier: int, name: str, /) -> None:
        self.id = identifier
        self.name = name


class Car:
    __model__ = API_V1.model('Car', {
        'id': fields.Integer(readonly=True, min=1, description='The car id'),
        'model': fields.String(required=True, description='The car model'),
        'brand': fields.Nested(Brand.__model__,
                               allow_null=False,
                               skip_none=True,
                               description='The car brand')
    })

    def __init__(self, identifier: int, model: str, brand: Brand) -> None:
        self.id = identifier
        self.model = model
        self.brand = brand


class Customer:
    __model__ = API_V1.model('Customer', {
        'id': fields.Integer(readonly=True, min=1, description='The customer id'),
        'fullname': fields.String(required=True, description='The customer fullname'),
        'cars': fields.List(fields.Nested(Car.__model__,
                                          allow_null=False,
                                          skip_none=True,
                                          description='The customers cars'))
    })

    def __init__(self, identifier: int, fullname: str,
                 cars: Optional[List[Car]] = None, /) -> None:
        self.id = identifier
        self.fullname = fullname
        self.cars = cars or []


class User:
    __model_signin__ = API_V1.model('User sign in', {
        'username': fields.String(required=True, description='The username'),
        'password': fields.String(required=True, description='The user password')
    })

    def __init__(self, identifier: int, username: str, password: str,
                 role: Optional[str] = None, /) -> None:
        from werkzeug.security import generate_password_hash
        self.id = identifier
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role


class UserToken:
    def __init__(self, user_id: int, auth_token: AuthToken, /) -> None:
        self.user_id = user_id
        self.auth_token = auth_token

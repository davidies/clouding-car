import datetime as dt
import jwt
import uuid
from flask import current_app, request
from http import HTTPStatus
from typing import Iterable, Optional, Union
from .. import API_V1
from ..shared.constants import BEARER_TOKEN_REQUIRED, NOT_ENOUGH_PERMISSIONS


def generate_access_token(username: str, role: str, /) -> str:
    claims = {'iss': request.host,
              'sub': username,
              'aud': 'https://myexample.com',
              'exp': dt.datetime.utcnow() + dt.timedelta(minutes=15),
              'iat': dt.datetime.utcnow(),
              'jti': str(uuid.uuid4()),
              'role': role}
    return jwt.encode(claims, current_app.config['SECRET_KEY']).decode('utf-8')


def token_required(roles: Optional[Union[str, Iterable[str]]] = None):
    def outer_wrapper(f):
        def inner_wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer'):
                access_token = auth_header.split()[1]
                options = {'verify_aud': True, 'verify_iss': True}
                try:
                    decoded_token = jwt.decode(access_token,
                                               current_app.config['SECRET_KEY'],
                                               options=options,
                                               audience='https://myexample.com',
                                               issuer=request.host)
                    role = decoded_token.get('role')
                    if roles and role:
                        if type(roles) is str:
                            if role != roles:
                                API_V1.abort(HTTPStatus.FORBIDDEN,
                                             NOT_ENOUGH_PERMISSIONS)
                        else:
                            if role not in roles:
                                API_V1.abort(HTTPStatus.FORBIDDEN,
                                             NOT_ENOUGH_PERMISSIONS)
                except jwt.PyJWTError as error:
                    API_V1.abort(HTTPStatus.UNAUTHORIZED, error.args[0])
            else:
                API_V1.abort(HTTPStatus.UNAUTHORIZED, BEARER_TOKEN_REQUIRED)
            return f(*args, **kwargs)
        return inner_wrapper
    return outer_wrapper

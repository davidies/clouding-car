import datetime as dt
import jwt
import uuid
from flask import current_app, request


def generate_access_token(username: str, role: str, /) -> str:
    claims = {'iss': request.host,
              'sub': username,
              'aud': 'https://myexample.com',
              'exp': dt.datetime.utcnow() + dt.timedelta(minutes=15),
              'iat': dt.datetime.utcnow(),
              'jti': str(uuid.uuid4()),
              'role': role}
    return jwt.encode(claims, current_app.config['SECRET_KEY']).decode('utf-8')

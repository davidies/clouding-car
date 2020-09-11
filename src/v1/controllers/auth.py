import secrets
from flask_restplus import fields, Namespace, Resource
from http import HTTPStatus
from .. import API_V1
from ..models import AuthToken, User, UserToken
from ..repos import USERS, USER_TOKENS
from ..shared.constants import INVALID_CREDENTIALS, INVALID_REFRESH_TOKEN, SUCCESSFUL_LOGIN
from ..shared.utils import generate_access_token

AUTH_NS = Namespace('auth')


REFRESH_TOKEN_MODEL = API_V1.model('RefreshToken', {
    'refresh_token': fields.String(required=True)})


@AUTH_NS.route('/refresh')
class Refresh(Resource):
    @AUTH_NS.expect(REFRESH_TOKEN_MODEL, validate=True)
    @AUTH_NS.marshal_with(AuthToken.__model__,
                          code=HTTPStatus.OK,
                          description=SUCCESSFUL_LOGIN)
    @AUTH_NS.response(HTTPStatus.BAD_REQUEST, INVALID_CREDENTIALS)
    def post(self) -> (AuthToken, HTTPStatus):
        refresh_token = API_V1.payload['refresh_token']
        user_token = None
        for ut in USER_TOKENS:
            if ut.auth_token.refresh_token == refresh_token:
                user_token = ut
                break
        if user_token:
            user = next(filter(lambda u: u.id == user_token.user_id, USERS))
            user_token.access_token = generate_access_token(user.username, user.role)
            user_token.refresh_token = secrets.token_hex(16)
            return user_token, HTTPStatus.OK
        else:
            AUTH_NS.abort(HTTPStatus.BAD_REQUEST, INVALID_REFRESH_TOKEN)


@AUTH_NS.route('/sign-in')
class SignIn(Resource):
    @AUTH_NS.expect(User.__model_signin__, validate=True)
    @AUTH_NS.marshal_with(AuthToken.__model__,
                          code=HTTPStatus.OK,
                          description=SUCCESSFUL_LOGIN)
    @AUTH_NS.response(HTTPStatus.BAD_REQUEST, INVALID_CREDENTIALS)
    def post(self) -> (AuthToken, HTTPStatus):
        from werkzeug.security import check_password_hash
        username = API_V1.payload['username']
        password = API_V1.payload['password']
        user = None
        for u in USERS:
            if u.username == username:
                user = u
                break
        if user and check_password_hash(user.password, password):
            access_token = generate_access_token(username, user.role)
            refresh_token = secrets.token_hex(16)
            auth_token = AuthToken(access_token, refresh_token)
            USER_TOKENS.append(UserToken(user.id, auth_token))
            return auth_token, HTTPStatus.OK
        else:
            AUTH_NS.abort(HTTPStatus.BAD_REQUEST, INVALID_CREDENTIALS)

from flask_restplus import fields
from .. import API_V1


class Brand:
    __model__ = API_V1.model('Brand', {
        'id': fields.Integer(readonly=True, min=1, description='The brand id'),
        'name': fields.String(required=True, description='The brand name')
    })

    def __init__(self, identifier: int, name: str, /) -> None:
        self.id = identifier
        self.name = name


class Customer:
    __model__ = API_V1.model('Customer', {
        'id': fields.Integer(readonly=True, min=1, description='The customer id'),
        'fullname': fields.String(required=True, description='The customer fullname')
    })

    def __init__(self, identifier: int, fullname: str, /) -> None:
        self.id = identifier
        self.fullname = fullname

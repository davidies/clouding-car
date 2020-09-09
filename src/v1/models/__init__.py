from flask_restplus import fields
from .. import API_V1


class Customer:
    __model__ = API_V1.model('Customer', {
        'id': fields.Integer(readonly=True, min=1, description='The customer id'),
        'fullname': fields.String(required=True, description='The customer fullname')
    })

    def __init__(self, identifier: int, fullname: str, /) -> None:
        self.id = identifier
        self.fullname = fullname

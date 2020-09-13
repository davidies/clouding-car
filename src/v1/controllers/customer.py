from flask import request
from flask_restplus import fields, Namespace, Resource
from http import HTTPStatus
from typing import Dict, List
from .. import API_V1
from ..models import Customer
from ..repos import CUSTOMERS
from ..shared.constants import (AUTHORIZATION_HEADER_DESC, NOT_FOUND,
                                SUCCESSFULLY_ADDED, SUCCESSFULLY_DELETED,
                                SUCCESSFULLY_UPDATED)
from ..shared.utils import token_required


CUSTOMER_NS = Namespace('customers')


@CUSTOMER_NS.route('/')
class CustomerList(Resource):
    @CUSTOMER_NS.header('Authorization', AUTHORIZATION_HEADER_DESC)
    @CUSTOMER_NS.marshal_list_with(Customer.__model__)
    @token_required()
    def get(self) -> (List[Customer], HTTPStatus):
        return CUSTOMERS, HTTPStatus.OK

    @CUSTOMER_NS.expect(Customer.__model__, validate=True)
    @CUSTOMER_NS.header('Authorization', AUTHORIZATION_HEADER_DESC)
    @CUSTOMER_NS.marshal_with(Customer.__model__,
                              code=HTTPStatus.CREATED,
                              description=SUCCESSFULLY_ADDED)
    @token_required(roles={'admin', 'salesperson'})
    def post(self) -> (Customer, HTTPStatus, Dict[str, str]):
        if CUSTOMERS:
            identifier = max(map(lambda c: c.id, CUSTOMERS)) + 1
        else:
            identifier = 1
        fullname = API_V1.payload['fullname']
        customer = Customer(identifier, fullname)
        CUSTOMERS.append(customer)
        headers = {'Location': f'{request.base_url}{identifier}'}
        return customer, HTTPStatus.CREATED, headers


@CUSTOMER_NS.route('/<int:identifier>')
class CustomerSingle(Resource):
    @CUSTOMER_NS.header('Authorization', AUTHORIZATION_HEADER_DESC)
    @CUSTOMER_NS.marshal_with(Customer.__model__)
    @CUSTOMER_NS.response(HTTPStatus.NOT_FOUND, NOT_FOUND)
    @token_required()
    def get(self, identifier: int) -> (Customer, HTTPStatus):
        for customer in CUSTOMERS:
            if customer.id == identifier:
                return customer, HTTPStatus.OK
        CUSTOMER_NS.abort(HTTPStatus.NOT_FOUND,
                          f'Customer not found with id: {identifier}')

    @CUSTOMER_NS.header('Authorization', AUTHORIZATION_HEADER_DESC)
    @CUSTOMER_NS.expect(Customer.__model__, validate=True)
    @CUSTOMER_NS.response(HTTPStatus.NO_CONTENT, SUCCESSFULLY_UPDATED)
    @CUSTOMER_NS.response(HTTPStatus.NOT_FOUND, NOT_FOUND)
    @token_required(roles={'admin', 'salesperson'})
    def put(self, identifier: int) -> (None, HTTPStatus):
        for customer in CUSTOMERS:
            if customer.id == identifier:
                customer.fullname = API_V1.payload['fullname']
                return None, HTTPStatus.NO_CONTENT
        CUSTOMER_NS.abort(HTTPStatus.NOT_FOUND,
                          f'Customer not found with id: {identifier}')

    @CUSTOMER_NS.header('Authorization', AUTHORIZATION_HEADER_DESC)
    @CUSTOMER_NS.response(HTTPStatus.NO_CONTENT, SUCCESSFULLY_DELETED)
    @token_required(roles='admin')
    def delete(self, identifier: int) -> (None, HTTPStatus):
        for customer in CUSTOMERS:
            if customer.id == identifier:
                CUSTOMERS.remove(customer)
                break
        return None, HTTPStatus.NO_CONTENT

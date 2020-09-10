from flask import request
from flask_restplus import fields, Namespace, Resource
from http import HTTPStatus
from typing import Dict, List
from .. import API_V1
from ..models import Brand
from ..repos import BRANDS
from ..shared.constants import NOT_FOUND, SUCCESSFULLY_ADDED


BRAND_NS = Namespace('brands')


@BRAND_NS.route('/')
class BrandList(Resource):
    @BRAND_NS.marshal_list_with(Brand.__model__)
    def get(self) -> (List[Brand], HTTPStatus):
        return BRANDS, HTTPStatus.OK

    @BRAND_NS.expect(Brand.__model__, validate=True)
    @BRAND_NS.marshal_with(Brand.__model__,
                           code=HTTPStatus.CREATED,
                           description=SUCCESSFULLY_ADDED)
    def post(self) -> (Brand, HTTPStatus, Dict[str, str]):
        if BRANDS:
            identifier = max(map(lambda b: b.id, BRANDS)) + 1
        else:
            identifier = 1
        name = API_V1.payload['name']
        brand = Brand(identifier, name)
        BRANDS.append(brand)
        headers = {'Location': f'{request.base_url}{identifier}'}
        return brand, HTTPStatus.CREATED, headers


@BRAND_NS.route('/<int:identifier>')
class BrandSingle(Resource):
    @BRAND_NS.marshal_with(Brand.__model__)
    @BRAND_NS.response(HTTPStatus.NOT_FOUND, NOT_FOUND)
    def get(self, identifier: int) -> (Brand, HTTPStatus):
        for brand in BRANDS:
            if brand.id == identifier:
                return brand, HTTPStatus.OK
        BRAND_NS.abort(HTTPStatus.NOT_FOUND, f'Brand not found with id: {identifier}')

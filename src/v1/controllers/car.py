from flask import abort, request
from flask_restplus import Namespace, Resource
from http import HTTPStatus
from typing import Dict, List
from .. import API_V1
from ..models import Brand, Car
from ..repos import BRANDS, CARS
from ..shared.constants import NOT_FOUND, SUCCESSFULLY_ADDED, SUCCESSFULLY_DELETED


CAR_NS = Namespace('cars')


@CAR_NS.route('/')
class CarList(Resource):
    @CAR_NS.marshal_list_with(Car.__model__)
    def get(self) -> (List[Car], HTTPStatus):
        return CARS, HTTPStatus.OK

    @CAR_NS.expect(Car.__model__, validate=True)
    @CAR_NS.marshal_with(Car.__model__,
                         code=HTTPStatus.CREATED,
                         description=SUCCESSFULLY_ADDED)
    def post(self) -> (Car, HTTPStatus, Dict[str, str]):
        if CARS:
            identifier = max(map(lambda c: c.id, CARS)) + 1
        else:
            identifier = 1
        model = API_V1.payload['model']
        brand_id = API_V1.payload['brand']['id']
        brand = next(filter(lambda b: b.id == brand_id, BRANDS))
        car = Car(identifier, model, brand)
        CARS.append(car)
        headers = {'Location': f'{request.base_url}{identifier}'}
        return car, HTTPStatus.CREATED, headers


@CAR_NS.route('/<int:identifier>')
class CarSingle(Resource):
    @CAR_NS.marshal_with(Car.__model__)
    @CAR_NS.response(HTTPStatus.NOT_FOUND, NOT_FOUND)
    def get(self, identifier: int) -> (Car, HTTPStatus):
        for car in CARS:
            if car.id == identifier:
                return car, HTTPStatus.OK
        abort(HTTPStatus.NOT_FOUND, NOT_FOUND)
    
    @CAR_NS.response(HTTPStatus.NO_CONTENT, SUCCESSFULLY_DELETED)
    def delete(self, identifier: int) -> (None, HTTPStatus):
        for car in CARS:
            if car.id == identifier:
                CARS.remove(car)
        return None, HTTPStatus.NO_CONTENT

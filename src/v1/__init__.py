from flask import Blueprint
from flask_restplus import Api


BLUEPRINT_V1 = Blueprint('blueprint_v1', __name__)
API_V1 = Api(BLUEPRINT_V1, version='1.0', title='Clouding Car', license='MIT')

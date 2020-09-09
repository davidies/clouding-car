from flask import Blueprint
from flask_restplus import Api


BLUEPRINT_V1 = Blueprint('blueprint_v1', __name__)
API_V1 = Api(BLUEPRINT_V1, version='1.0', title='Clouding Car', license='MIT')


from .controllers import BRAND_NS, CUSTOMER_NS


API_V1.add_namespace(BRAND_NS)
API_V1.add_namespace(CUSTOMER_NS)

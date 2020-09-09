from flask import Flask
from .v1 import BLUEPRINT_V1

APP = Flask(__name__)
APP.register_blueprint(BLUEPRINT_V1, url_prefix='/api/v1', strict_slashes=False)

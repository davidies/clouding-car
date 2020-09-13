import os
from flask import Flask
from .v1 import BLUEPRINT_V1

APP = Flask(__name__)
if 'SECRET_KEY' in os.environ:
    APP.config['SECRET_KEY'] = os.environ['SECRET_KEY']
else:
    raise KeyError("'SECRET_KEY' was not set as enviroment variable")
APP.register_blueprint(BLUEPRINT_V1, url_prefix='/api/v1', strict_slashes=False)

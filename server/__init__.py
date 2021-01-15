from flask import Flask
from flask_cors import CORS
import logging


app = Flask(__name__)
app.debug = True
CORS(app)

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)

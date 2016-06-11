# __author__ = 'Slevin'
from flask import Blueprint

main = Blueprint('main', __name__)

from . import user

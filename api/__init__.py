from flask import Blueprint

api_bp = Blueprint('api',__name__, template_folder="template", static_folder="static")

from . import routes

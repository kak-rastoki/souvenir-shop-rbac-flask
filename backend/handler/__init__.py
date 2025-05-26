from flask import Blueprint

handler_bp = Blueprint('handler', __name__, template_folder='templates', static_folder='static')

from handler import handlers

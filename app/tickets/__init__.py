from flask import Blueprint

bp = Blueprint('tickets', __name__, template_folder='templates')

from app.tickets import routes
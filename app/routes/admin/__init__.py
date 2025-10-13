from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix = '/admin')

from . import dashboard
from . import add_doctor
from . import add_patient
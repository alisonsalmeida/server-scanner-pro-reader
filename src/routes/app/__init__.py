from sanic.blueprints import Blueprint
from .user import user
from .sheet import sheet


app = Blueprint.group(user, sheet, url_prefix='/app')

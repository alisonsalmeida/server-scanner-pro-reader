from sanic import Blueprint
from sanic.request import Request
from src.controllers import SessionController


session = Blueprint('session', url_prefix='/session')


@session.post('/')
async def get(request: Request):
    return await SessionController.store(request)

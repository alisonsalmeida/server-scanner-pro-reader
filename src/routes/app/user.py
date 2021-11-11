from sanic import Blueprint, response
from sanic.request import Request
from src.controllers.app import UserController


user = Blueprint('user', url_prefix='/user')


@user.middleware('request')
async def middleware(request: Request):
    pass


@user.get('/<_id>')
async def show(request: Request, _id: str):
    return response.json({})


@user.post('/')
async def store(request: Request):
    return await UserController.store(request)


@user.put('/<_id>')
async def update(request: Request, _id: str):
    return response.json({})

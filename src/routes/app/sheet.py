from sanic import Blueprint, response
from sanic.request import Request
from src.controllers import SheetController, authorization


sheet = Blueprint('sheet', url_prefix='/sheet')


@sheet.middleware('request')
async def middleware(request: Request):
    pass


@sheet.get('/')
@authorization()
async def index(request: Request):
    return await SheetController.index(request)


@sheet.get('/<_id>')
@authorization()
async def show(request: Request, _id: str):
    return await SheetController.show(request, _id)


@sheet.post('/')
@authorization()
async def store(request: Request):
    return await SheetController.store(request)


@sheet.delete('/<_id>')
@authorization()
async def destroy(request: Request, _id: str):
    return await SheetController.destroy(request, _id)


@sheet.put('/<_id>')
@authorization()
async def update(request: Request, _id: str):
    return await SheetController.update(request, _id)

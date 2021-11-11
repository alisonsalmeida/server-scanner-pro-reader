from sanic import Blueprint, response, exceptions
from sanic.request import Request
from .app import app
from .session import session


routes = Blueprint.group(app, session, url_prefix='/')


@routes.middleware('request')
async def middleware(request: Request):
    page = 0
    size = 10
    sizes = [10, 20, 50]

    if 'page' not in request.args:
        request.args['page'] = page

    else:
        _page = request.args['page'][0]
        if isinstance(_page, str):
            if _page.isnumeric():
                page = int(_page)

            else:
                return response.json({'message', 'Page must be numeric'}, status=400)

        elif isinstance(_page, int):
            page = _page

        else:
            return response.json({'message', f'The {type(_page)} is not an valid type'}, status=400)

        request.args['page'] = page

    if 'size' not in request.args:
        request.args['size'] = size

    else:
        _size = request.args['size']
        if isinstance(_size, str):
            if _size.isnumeric():
                _size = int(_size)

            else:
                return response.json({'message', 'Size must be numeric'}, status=400)

        elif isinstance(_size, int):
            pass

        else:
            return response.json({'message', f'The {type(_size)} is not an valid type'}, status=400)

        if _size in sizes:
            size = _size

        request.args['size'] = size

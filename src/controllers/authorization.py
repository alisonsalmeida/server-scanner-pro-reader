from sanic.request import Request
from sanic import response
from functools import wraps
from src.utils import env

import jwt


def authorization():
    def decorator(func):
        @wraps(func)
        async def _decorator(request: Request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            if request.token is None:
                return response.json({'message': 'token not provided'}, status=400)

            try:
                token = jwt.decode(request.token, env('APP_SECRET'), algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                return response.json({'message': 'Expired token'}, status=401)

            except jwt.DecodeError:
                return response.json({'message': 'Invalid token'}, status=401)

            except jwt.InvalidTokenError:
                return response.json({'message': 'Invalid token'}, status=401)

            request.headers['user'] = token['user']
            return await func(request, *args, **kwargs)

        return _decorator
    return decorator

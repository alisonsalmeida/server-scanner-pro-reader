from sanic.request import Request
from sanic import response, exceptions
from src.database import connection
from src.models import User
from src.utils import Serialize

import json


class UserController:
    @staticmethod
    async def store(request: Request):
        with connection.atomic() as transaction:
            errors = User.validate(request.json)
            if bool(errors):
                return response.json(errors, status=400)

            user = User.create(**request.json)

        return response.json(user.json, dumps=json.dumps, cls=Serialize)

from sanic.request import Request
from sanic import response
from src.database import connection
from src.models import User
from src.utils import env, Serialize
from datetime import datetime, timedelta

import json
import bcrypt
import jwt


class SessionController:
    @staticmethod
    async def store(request: Request):
        with connection.atomic() as transaction:
            username = request.json['username'] if 'username' in request.json else None
            email = request.json['email'] if 'email' in request.json else None
            password: str = request.json['password'] if 'password' in request.json else None

            if None in (username, password) and None in (email, password):
                return response.json({'message': 'Email or username and password is required'}, status=400)

            query = dict()
            if username is not None:
                query['username'] = username

            elif email is not None:
                query['email'] = email

            user = User.get_or_none(**query)

            if user is None:
                return response.json({'message': 'Username and password incorrect'}, status=401)

            if not bcrypt.checkpw(password.encode(), user.password.encode()):
                return response.json({'message': 'Username and password incorrect'}, status=401)

            expired = datetime.utcnow() + timedelta(minutes=30)
            token = jwt.encode(
                {'user': user._id, 'exp': expired},
                env('APP_SECRET'),
                algorithm='HS256'
            )

            data = dict(token=token, user=user.json)

        return response.json(data, status=200, dumps=json.dumps, cls=Serialize)

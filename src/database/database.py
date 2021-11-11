import hashlib

from peewee import PostgresqlDatabase, Model
from peewee_validates import ModelValidator
from playhouse.shortcuts import model_to_dict
from src.utils import env
from datetime import datetime

import peewee
import bcrypt


connection = PostgresqlDatabase(
    env('DATABASE_NAME'),
    user=env('DATABASE_USER'),
    password=env('DATABASE_PASS'),
    host=env('DATABASE_HOST'),
    port=int(env('DATABASE_PORT'))
)


class BaseModel(Model):
    class Meta:
        database = connection

    @property
    def json(self):
        return None

    @json.getter
    def json(self) -> dict:
        return model_to_dict(self, backrefs=True, recurse=False)

    @property
    def exclude(self):
        return None

    @exclude.getter
    def exclude(self):
        return ()

    @property
    def only(self):
        return None

    @only.getter
    def only(self):
        return ()

    @classmethod
    def validate(cls, data, only=None, exclude=None) -> dict:
        validator = ModelValidator(cls(**data))
        validator.validate(only=only, exclude=exclude)

        return validator.errors


class PrimaryKey(peewee.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(primary_key=True, default=self.generate, *args, **kwargs)

    def generate(self) -> str:
        seed = int(datetime.utcnow().timestamp())
        return hashlib.md5(str(seed).encode()).hexdigest()


class PasswordField(peewee.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_value(self, value: str):
        if value is not None:
            return bcrypt.hashpw(value.encode(), bcrypt.gensalt(14)).decode()

        return value


class FileField(peewee.CharField):
    def __init__(self, extension: str, *args, **kwargs):
        self.extension = extension
        super().__init__(default=self.generate, *args, **kwargs)

    def generate(self):
        pass

    def db_value(self, value):
        seed = int(datetime.utcnow().timestamp())
        hashed = hashlib.md5(str(seed).encode()).hexdigest()
        with open(f'./storage/{hashed}.{self.extension}', 'a') as fs:
            pass

        return hashed

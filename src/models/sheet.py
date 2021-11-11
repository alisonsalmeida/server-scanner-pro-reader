from src.database import BaseModel, PrimaryKey, PasswordField, FileField
from datetime import datetime
from .user import User
from playhouse.postgres_ext import ArrayField
from playhouse.hybrid import hybrid_property
from playhouse.shortcuts import model_to_dict
from src.utils import env

import os
import peewee
import pandas as pd


class Sheet(BaseModel):
    _id = PrimaryKey()
    filename = FileField(extension='csv')
    name = peewee.CharField(unique=True)
    fields = ArrayField(peewee.CharField)
    user = peewee.ForeignKeyField(User, backref='sheets')

    createdAt = peewee.DateTimeField(default=datetime.utcnow())
    updatedAt = peewee.DateTimeField(default=datetime.utcnow())

    @hybrid_property
    def url(self):
        if isinstance(self, Sheet):
            return f"{env('APP_URL')}/files/{self.filename}.{Sheet.filename.extension}"

    def create_headers(self):
        path = f'./storage/{self.filename}.{Sheet.filename.extension}'
        df = pd.DataFrame(columns=self.fields)
        df.to_csv(path, sep=';')

    def update_file(self, values: list):
        path = f'./storage/{self.filename}.{Sheet.filename.extension}'
        df = pd.read_csv(path, sep=';', index_col=0)

        for value in values:
            df.loc[-1] = value
            df.index = df.index + 1

        df.to_csv(path, sep=';')

    @property
    def json(self):
        return None

    @json.getter
    def json(self):
        return model_to_dict(
            self,
            recurse=False,
            backrefs=True,
            exclude=self.exclude,
            only=self.only,
            extra_attrs=['url']
        )

    @property
    def exclude(self):
        return None

    @exclude.getter
    def exclude(self):
        return [Sheet.filename]

    def delete_instance(self, recursive=False, delete_nullable=False):
        path = f'./storage/{self.filename}.{Sheet.filename.extension}'
        try:
            os.remove(path)
        except FileNotFoundError as e:
            pass

        return super().delete_instance(recursive, delete_nullable)

    @classmethod
    def create(cls, **query):
        inst = super().create(**query)
        instance: Sheet = cls.get(_id=inst._id)
        instance.create_headers()

        return instance

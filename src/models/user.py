from src.database import BaseModel, PrimaryKey, PasswordField
from datetime import datetime
from playhouse.shortcuts import model_to_dict
from peewee_validates import ModelValidator, StringField, validate_email, validate_model_unique

import peewee


class UserValidator(ModelValidator):
    def add_validate_unique(self, fields: dict):
        for name, p_field in fields.items():
            field = self._meta.fields.get(name)
            field.validators.append(validate_model_unique(p_field, self.instance.select()))

    def validate(self, data=None, only=None, exclude=None):
        instance_unique = dict()
        for name, field in self.instance._meta.fields.items():
            if field.unique:
                instance_unique[name] = field

        self.add_validate_unique(instance_unique)
        super().validate(data, only, exclude)

    password = StringField(required=True, min_length=8)
    email = StringField(required=True, validators=[validate_email()])


class User(BaseModel):
    _id = PrimaryKey()
    name = peewee.CharField()
    username = peewee.CharField(unique=True)
    password = PasswordField()
    email = peewee.CharField(unique=True)
    confirmed = peewee.BooleanField(default=False)
    phone = peewee.CharField(null=True)

    createdAt = peewee.DateTimeField(default=datetime.utcnow())
    updatedAt = peewee.DateTimeField(default=datetime.utcnow())

    @property
    def exclude(self):
        return None

    @exclude.getter
    def exclude(self):
        return User.password, User.confirmed

    @property
    def json(self):
        return dict()

    @json.getter
    def json(self):
        return model_to_dict(
            self,
            exclude=self.exclude,
            only=self.only,
            backrefs=True,
            recurse=False
        )

    @classmethod
    def validate(cls, data, only=None, exclude=None) -> dict:
        validator = UserValidator(cls(**data))
        validator.validate(data, only=only, exclude=exclude)

        return validator.errors

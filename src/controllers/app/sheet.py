from sanic.request import Request
from sanic import response, exceptions
from src.models import Sheet
from src.database import connection
from typing import List
from src.utils import Serialize

import json


class SheetController:
    @staticmethod
    async def find(request: Request, _sheet: str) -> Sheet:
        """
        Verifica se a planilha identificada por _sheet existe
        :param request:
        :param _sheet:
        :return: Sheet
        """

        user = request.headers['user']
        sheet = Sheet.get_or_none(_id=_sheet)

        if sheet is None:
            raise exceptions.NotFound(f'Sheet {_sheet} not founded')

        if sheet.user._id != user:
            raise exceptions.Unauthorized(f'Sheet {_sheet} its not yours')

        return sheet

    @staticmethod
    async def index(request: Request):
        """
        Retorna as primeira 10 planilhas do usuario
        aceita page e size para a paginação
        :param request:
        :return:
        """
        with connection.atomic() as transaction:
            page = request.args['page']
            size = request.args['size']
            user = request.headers['user']

            query: List[Sheet] = Sheet.select().where(Sheet.user == user).paginate(page, paginate_by=size)
            sheets = []

            for sheet in query:
                sheets.append(sheet.json)

        return response.json(sheets, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def show(request: Request, sheet: str):
        """
        Retorna uma planilha identificada por sheet
        :param request:
        :param sheet:
        :return:
        """
        with connection.atomic() as transaction:
            sheet = await SheetController.find(request, sheet)
            return response.json(sheet.json, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def store(request: Request):
        """
        Cria uma nova planilha para o usuario
        :param request:
        :return:
        """
        with connection.atomic() as transaction:
            data = request.json
            data['user'] = request.headers['user']

            errors = Sheet.validate(request.json, exclude=['filename', 'fields'])
            if bool(errors):
                return response.json(errors, status=400)

            sheet = Sheet.create(**data)
            return response.json(sheet.json, dumps=json.dumps, cls=Serialize, status=201)

    @staticmethod
    async def destroy(request: Request, sheet: str):
        """
        Remove uma planilha identificada por sheet
        :param request:
        :param sheet:
        :return:
        """
        with connection.atomic() as transaction:
            sheet = await SheetController.find(request, sheet)
            sheet.delete_instance(True)

        return response.empty()

    @staticmethod
    async def update(request: Request, sheet):
        """
        Recebe novos dados para inserir na planilha
        :param request:
        :param sheet:
        :return:
        """
        with connection.atomic() as transaction:
            sheet = await SheetController.find(request, sheet)
            values = request.json['values']
            sheet.update_file(values)

            return response.empty()

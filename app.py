from asyncio.events import AbstractEventLoop
from datetime import datetime
from sanic import Sanic, response
from sanic.request import Request
from sanic.exceptions import NotFound

import pandas
import os


app = Sanic(__name__)


@app.route('/')
async def index(request: Request):
    return response.json({})


@app.route('/codes', methods=['GET', 'POST'])
async def index_codes(request: Request):
    print(request.json)

    if request.method == 'GET':
        return await response.file('codes.csv')
    
    elif request.method == 'POST':
        body: dict = request.json
        codesFrame = pandas.read_csv('codes.csv', sep=';', index_col=0)
        data = {'codigo': str(body['code']), 'descrição': str(body['description'])}

        newCode = pandas.Series(data=data, name=datetime.utcnow().isoformat())
        codesFrame = codesFrame.append(newCode)

        print(codesFrame)
        codesFrame.to_csv('codes.csv', sep=';')
        return response.empty()

    else:
        raise NotFound()


@app.listener('before_server_start')
async def create_file(server: Sanic, loop: AbstractEventLoop):
    if not os.path.isfile('codes.csv'):
        data = {'codigo': str(), 'descrição': str()}
        dataFrame = pandas.DataFrame(data=data, index=[datetime.utcnow().isoformat()])
        dataFrame.to_csv('codes.csv', sep=';')

    else:
        dataFrame = pandas.read_csv('codes.csv', sep=';', index_col=0)
        print(dataFrame)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, auto_reload=True)

import os.path
from asyncio.events import AbstractEventLoop
from sanic import Sanic, response
from src.routes import routes
from sanic.log import logger
from src.database import connection
from src.models import tables


app = Sanic(__name__)
app.config.FALLBACK_ERROR_FORMAT = "json"
app.blueprint(routes)


@app.listener('before_server_start')
async def create_tables(server: Sanic, loop: AbstractEventLoop):
    try:
        connection.create_tables(tables)
    except Exception as e:
        logger.info(f'error in create tables {e}')

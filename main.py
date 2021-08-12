import sys
from loguru import logger

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.graphql import GraphQLApp

from graphene import Schema

from routers.chat import chat
from routers.tasks import tasks
from routers.graphql import Query


def remove_all_existing_handlers():
    logger.remove()


remove_all_existing_handlers()
logger.add('app.log', level='WARNING', backtrace=True, diagnose=True)
logger.add(
    sys.stderr,
    format='<white>{level}</white> | {time: HH:mm:ss MM/DD} | <blue>{message}</blue>',
    colorize=True
)

logger.debug('Starting the main application ...')

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(chat)
app.include_router(tasks)
app.add_route('/graphql', GraphQLApp(schema=Schema(query=Query)))

logger.debug(
    'Successful start: routes and graphql included, static directory mounted.')

subapi = FastAPI()
logger.debug('Starting subapi ...')


@app.get('/', tags=['test'])
@logger.catch
async def index():
    '''Test index endpoint'''
    return {'foo': 'bar'}


@app.get('/hello', tags=['test'])
@logger.catch
async def test():
    ''' Test hello endpoint'''
    return {'hello': 'world'}


@app.on_event('startup')
@logger.catch
async def on_startup():
    print('Initializing the database')


@app.on_event('shutdown')
@logger.catch
async def on_shutdown():
    print('On shutdown')


@subapi.get('/', tags=['test'])
@logger.catch
async def sub_index():
    '''Test subapi index endpoint'''
    return {'foo': 'bar'}


@subapi.get('/hello', tags=['test'])
@logger.catch
async def sub_test():
    '''Test subapi hello endpoint'''
    return {'hello': 'world'}


app.mount('/subapi', subapi)
logger.debug('Subapi mounted successfully')

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.graphql import GraphQLApp
from graphene import Schema

from routers.chat import chat
from routers.tasks import tasks
from routers.graphql import Query


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(chat)
app.include_router(tasks)

subapi = FastAPI()


@app.get('/', tags=['test'])
async def index():
    '''Test index endpoint'''
    return {'foo': 'bar'}


@app.get('/hello', tags=['test'])
async def test():
    ''' Test hello endpoint'''
    return {'hello': 'world'}


@app.on_event('startup')
async def on_startup():
    print('Initializing the database')


@app.on_event('shutdown')
async def on_shutdown():
    print('On shutdown')


@subapi.get('/', tags=['test'])
async def sub_index():
    '''Test subapi index endpoint'''
    return {'foo': 'bar'}


@subapi.get('/hello', tags=['test'])
async def sub_test():
    '''Test subapi hello endpoint'''
    return {'hello': 'world'}


app.mount('/subapi', subapi)
app.add_route('/graphql', GraphQLApp(schema=Schema(query=Query)))

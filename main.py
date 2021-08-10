from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers.chat import chat
from routers.tasks import tasks


app = FastAPI()
# app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(chat)
app.include_router(tasks)

subapi = FastAPI()


@app.get('/', tags=['test'])
async def index():
    '''Test index endpoint'''
    return {'foo': 'bar'}


@app.get('/hello', tags=['test'])
async def test():
    '''Test hello endpoint'''
    return {'hello': 'world'}


@subapi.get('/')
async def sub_index():
    '''Test subapi index endpoint'''
    return {'foo': 'bar'}


@subapi.get('/hello')
async def sub_test():
    '''Test subapi hello endpoint'''
    return {'hello': 'world'}


app.mount('/subapi', subapi)

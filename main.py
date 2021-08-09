from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers.chat import chat
from routers.tasks import tasks


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(chat)
app.include_router(tasks)


@app.get('/hello', tags=['test'])
async def test():
    '''Test endpoint'''
    return {'hello': 'world'}

from fastapi import FastAPI
from pydantic import BaseModel

from worker import queue, sleep_task


app = FastAPI()


class JobOut(BaseModel):
    key: str
    info: str


@app.get('/hello', tags=['test'])
def test():
    '''Test endpoint'''
    return {'hello': 'world'}


@app.post('/tasks/{seconds}', response_model=JobOut, status_code=201, tags=['tasks'])
def add_task(seconds: int):
    '''
    Adds tasks to worker queue.
    Expects body as dictionary matching the Group class.
    '''
    job = queue.enqueue(sleep_task, seconds)
    return JobOut(info=job.__repr__(), key=job.key)


@app.get('/queue-size', tags=['tasks'])
def queue_size():
    '''Test endpoint'''
    return {'Queue Size': len(queue)}

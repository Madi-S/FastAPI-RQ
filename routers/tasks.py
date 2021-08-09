from fastapi import APIRouter
from pydantic import BaseModel

from worker import queue, sleep_task


tasks = APIRouter(prefix='/tasks')


class JobOut(BaseModel):
    key: str
    info: str


@tasks.post('/{seconds}', response_model=JobOut, status_code=201, tags=['tasks'])
async def add_task(seconds: int):
    '''
    Adds tasks to worker queue.
    Expects body as dictionary matching the Group class.
    '''
    job = queue.enqueue(sleep_task, seconds)
    return JobOut(info=job.__repr__(), key=job.key)


@tasks.get('/queue-size', tags=['tasks'])
async def queue_size():
    '''Test endpoint'''
    return {'Queue Size': len(queue)}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import Redis
from rq import Queue

from worker import sleep_task

app = FastAPI()

redis_conn = Redis(host='myproj_redis', port=6379)
q = Queue('my_queue', connection=redis_conn)

@app.get('/hello')
def test():
    '''Test endpoint'''
    return {'hello': 'world'}


@app.post('/groups/{seconds}', status_code=201)
def add_task(seconds: int):
    '''
    Adds tasks to worker queue.
    Expects body as dictionary matching the Group class.
    '''

    job = q.enqueue(sleep_task, seconds)
    print(dir(job), job)

    return {'job': job.__repr__, 'key': job.key}


@app.get('/query-size')
def query_size():
    '''Test endpoint'''
    return {'Queue Size': len(q)}
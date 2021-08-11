import requests
from redis import Redis
from rq import Queue

from time import sleep

from config import API_URL


REDIS_HOST = 'redis'
REDIS_PORT = 6379
QUEUE_NAME = 'my_queue'

redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
queue = Queue(QUEUE_NAME, connection=redis)


def greet_task(name: str):
    print(f'Greetings, {name}!')


def request_task():
    response = requests.get(API_URL + '/test')
    print(response)


def sleep_task(seconds: int = 10):
    print('Starting the task ...')
    sleep(seconds)

    print('Finished the task ...')
    return {'status': 'completed'}


'''
RQ Scheduler is flawed, so it is better to pass on this

from rq_scheduler import Scheduler
from datetime import datetime


scheduler = Scheduler(connection=redis)

scheduler.schedule(
    scheduled_time=datetime.utcnow(),
    func=greet,
    args=['Romelu Lukaku'],
    interval=10,
)

scheduler.schedule(
    scheduled_time=datetime.utcnow(),
    func=request_test,
    interval=10,
)

'''

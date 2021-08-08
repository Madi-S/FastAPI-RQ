from redis import Redis
from rq import Queue

from time import sleep


REDIS_HOST = 'redis'
REDIS_PORT = 6379
QUEUE_NAME = 'my_queue'

redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
queue = Queue(QUEUE_NAME, connection=redis_conn)


def sleep_task(seconds: int = 5):
    print('Starting the task ...')
    sleep(seconds)

    print('Finished the task ...')
    return {'status': 'completed'}

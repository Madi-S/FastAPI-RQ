from utils import clear_queue
from worker import queue, sleep_task, greet_task


def test_sleep_task(test_app):
    clear_queue()
    
    job = queue.enqueue(sleep_task, 2)
    assert job
    assert job.key
    assert_something_in_queue()


def test_greet_task(test_app):
    clear_queue()

    job = queue.enqueue(greet_task, 'John')
    assert job
    assert_something_in_queue()


def assert_something_in_queue():
    assert len(queue) > 0

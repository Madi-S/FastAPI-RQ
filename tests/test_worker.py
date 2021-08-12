from utils import clear_queue
from worker import queue, sleep_task, greet_task


def test_sleep_task(test_app):
    def assert_job(job):
        assert job
        assert job.key

    def create_sleep_task():
        return queue.enqueue(sleep_task, 2)

    clear_queue()

    job = create_sleep_task()

    assert_job(job)
    assert_something_in_queue()


def test_greet_task(test_app):
    def create_greet_task():
        return queue.enqueue(greet_task, 'John')

    clear_queue()

    job = create_greet_task()

    assert job
    assert_something_in_queue()


def assert_something_in_queue():
    assert len(queue) > 0

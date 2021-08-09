from utils import create_n_tasks


SLEEP_TASK_ARG = 1000
QUEUE_SIZE = 10

def test_add_task(test_app):
    response = test_app.get(f'/tasks/{SLEEP_TASK_ARG}')
    assert response.status_code == 200

    data = response.json()
    assert data.get('key')
    assert data.get('info')


def test_queue_size(test_app):
    create_n_tasks(QUEUE_SIZE)
    
    response = test_app.get(f'/tasks/queue-size')
    assert response.status_code == 200
    assert response.json().get('Queue Size') == QUEUE_SIZE
    
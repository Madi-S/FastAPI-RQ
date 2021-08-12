from utils import create_n_tasks, clear_queue


SLEEP_TASK_ARG = 100
QUEUE_SIZE = 10


def test_add_task(test_app):
    def assert_json_has_fields(data):
        assert data.get('key')
        assert data.get('info')
    
    clear_queue()
    
    response = test_app.post(f'/tasks/{SLEEP_TASK_ARG}')
    
    assert response.status_code == 201
    assert_json_has_fields(response.json)
    


def test_queue_size(test_app):
    clear_queue()
    create_n_tasks(QUEUE_SIZE)
    
    response = test_app.get(f'/tasks/queue-size')
    
    assert response.status_code == 200
    data = response.json()
    assert data.get('Queue Size') == QUEUE_SIZE

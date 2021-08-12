from utils import assert_response_code_and_json


def test_index(test_app):
    response = test_app.get('/')
    expected_json = {'foo': 'bar'}
    assert_response_code_and_json(response, 200, expected_json)


def test_hello(test_app):
    response = test_app.get('/hello')
    expected_json = {'hello': 'world'}
    assert_response_code_and_json(response, 200, expected_json)

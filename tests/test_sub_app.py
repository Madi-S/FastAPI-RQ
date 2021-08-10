

def test_index(test_app):
    response = test_app.get('/subapi/')
    assert response.status_code == 200
    assert response.json() == {'foo': 'bar'}


def test_hello(test_app):
    response = test_app.get('/subapi/hello')
    assert response.status_code == 200
    assert response.json() == {'hello': 'world'}

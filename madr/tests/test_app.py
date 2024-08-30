from http import HTTPStatus


def test_app(client):
    response = client.get('/health')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': 'OK'}

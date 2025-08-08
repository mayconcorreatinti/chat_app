from fastapi.testclient import TestClient
from app.main import app
from http import HTTPStatus


def test_get_users():
    client = TestClient(app)
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
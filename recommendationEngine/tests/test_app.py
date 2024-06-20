import pytest
from app import App

@pytest.fixture
def client():
    app_instance = App().app
    app_instance.config['TESTING'] = True
    with app_instance.test_client() as client:
        yield client

def test_recommendations(client):
    response = client.get('/recommendations')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 3
    for product in data:
        assert 'id' in product
        assert 'name' in product
        assert 'description' in product
        assert 'price' in product

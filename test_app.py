import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Testa se a rota principal retorna status 200"""
    response = client.get('/')
    assert response.status_code == 200


def test_pontos_sem_parametro(client):
    response = client.get('/pontos')
    assert response.status_code == 400
    data = response.get_json()
    assert data['erro'] == "Endereço não fornecido"


def test_detalhes_sem_xid(client):
    response = client.get('/detalhes')
    assert response.status_code == 400
    data = response.get_json()
    assert data['erro'] == "XID não fornecido"

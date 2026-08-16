def test_read_users_empty(client): 
    response = client.get('/users')

    assert response.status_code == 200
    assert response.json() == []


def test_create_user(client): 
    user_payload = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123"
    }
    response = client.post('/register', json=user_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"
    assert "id" in data


def test_create_and_read_one_user(client):
    user_payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "password": "password123"
    }
    # 1. Crear
    create_response = client.post('/register', json=user_payload)
    assert create_response.status_code == 200

    # 2. Consultar lista para verificar persistencia en memoria
    list_response = client.get('/users')
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["email"] == user_payload["email"]
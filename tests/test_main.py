from fastapi.testclient import TestClient
from user import User

from app.main import app


client = TestClient(app) 

def test_read_users_empty(): 
    response = client.get('/users')

    assert response.status_code == 200
    assert response.json() == []

def test_create_user(mock_db_session): 
    user = User(name="John Doe", email="john.doe@example.com", password="password123")
    response = client.post('/register', json=user.to_json())

    assert response.status_code == 200
    
    data = response.json()
    assert data == user.to_json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"

    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_create_and_read_one_user():
    user = User(name="John Doe", email="john.doe@example.com", password="password123")
    response = client.post('/register', json=user.to_json())

    user_email = response.json().get('email')

    assert user_email == user.email
    assert response.status_code == 200
    assert response.json() == user.to_json()

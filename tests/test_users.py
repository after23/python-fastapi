import pytest
from app import models, schemas
from .database import client, session
from jose import jwt
from app.config import settings
    

# def test_root(client):
#     response = client.get("/")
#     print(response.json().get('message'))
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World"}

@pytest.fixture()
def test_user(client):
    user_data = {"email": "test_user@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user

def test_create_user(client):
    res = client.post("/users/", json={"email": "testemail@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "testemail@gmail.com"

def test_login(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
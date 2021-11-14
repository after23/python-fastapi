from app import models, schemas
from .database import client, session
    

def test_root(client):
    response = client.get("/")
    print(response.json().get('message'))
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user(client):
    res = client.post("/users/", json={"email": "testemail@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "testemail@gmail.com"

def test_login(client):
    res = client.post("/login", data={"username": "testemail@gmail.com", "password": "password123"})

    assert res.status_code == 200
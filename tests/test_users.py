import pytest
from app import models, schemas
from jose import jwt
from app.config import settings
    

# def test_root(client):
#     response = client.get("/")
#     print(response.json().get('message'))
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World"}

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

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 403),
    ("test_user@gmail.com", "wrongpassword123", 403),
    ("wrongemail@gmail.com", "wrongpassword123", 403),
    (None, "password123", 422),
    ("test_user@gmail.com", None, 422)
])

def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == "Invalid Credentials"
from .utils import test_todo, override_get_db, override_get_current_user, \
    TestingSessionLocal, test_user, client, engine
from ..main import app
from ..routers.users import get_db, get_current_user
from fastapi import status
from fastapi.testclient import TestClient
from ..models import Users

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

print("Engine URL:", engine.url)


def test_return_user(test_user):
    response = client.get('/users/')
    print("Engine URL:", engine.url)
    print("Response JSON:", response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'whysamay'
    assert response.json()['email'] == "samaypawar2200@gmail.com"
    assert response.json()['first_name'] == 'samay'
    assert response.json()['last_name'] == 'pawar'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '111111111'


def test_change_password_success(test_user):
    response = client.put("/users/user/password", json={'password': 'testpassword',
                                                      'new_password': 'newpassword'})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_failure(test_user):
    response = client.put("/users/user/password", json={'password': 'testssword',
                                                        'new_password': 'newpassword'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}


def test_change_phone_number_success(test_user):
    new_phone = "222222222"
    response = client.put(f"/users/user/phone/{new_phone}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    updated_user = db.query(Users).filter(Users.id == test_user.id).first()
    assert updated_user.phone_number == new_phone


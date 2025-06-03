from starlette import status
from ..main import app
from ..models import Todos
from ..routers.admin import get_db, get_current_user
from .utils import test_todo, client, override_get_db, override_get_current_user, \
    TestingSessionLocal  # Import from utils.py

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all(test_todo):
    response = client.get('/admin/todo')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': 1,
        'title': 'learntocode',
        'description': 'learneveryday',
        'priority': 5,
        'complete': False,
        'owner_id': 1
    }]


def test_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete("/admin/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}


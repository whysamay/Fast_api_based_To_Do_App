import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from ..database import Base
from fastapi.testclient import TestClient
from ..main import app
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
        # only code before yield is executed before sending a respone and later code is run after sending a response
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'whysamay', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title='learntocode',
        description="learneveryday",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture()
def test_user():
    user = Users(
        username="whysamay",
        email="samaypawar2200@gmail.com",
        first_name="samay",
        last_name='pawar',
        hashed_password=bcrypt_context.hash("testpassword"),
        role='admin',
        phone_number='111111111'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
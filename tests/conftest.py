import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, TEST_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from app.config import settings
from app.utils.auth import create_access_token
from app.schemas import UserCreate
from app.crud import create_user
from app.models import User

# Используем тестовую базу данных
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def db_engine():
    if not database_exists(test_engine.url):
        create_database(test_engine.url)

    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    drop_database(test_engine.url)


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    connection.close()
    transaction.rollback()


@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[app.get_db] = override_get_db  # Используем app.get_db
    return TestClient(app)


@pytest.fixture(scope="module")
def test_user(client):
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "is_admin": True
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 200
    user = response.json()
    user["plain_password"] = user_data["password"]
    return user


@pytest.fixture(scope="module")
def token(test_user, client):
    login_data = {
        "username": test_user["username"],
        "password": test_user["plain_password"]
    }
    response = client.post("/api/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token


@pytest.fixture(scope="module")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from src.app.schemas.user import User
from src.app.core.security import get_password_hash, create_access_token
from datetime import timedelta
from src.app.config import get_settings
from src.app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Add superuser
        superuser = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            hashed_password=get_password_hash("adminpass"),
            is_superuser=True,
        )
        session.add(superuser)
        # Add regular user
        regular = User(
            first_name="Regular",
            last_name="User",
            email="user@example.com",
            hashed_password=get_password_hash("userpass"),
            is_superuser=False,
        )
        session.add(regular)
        session.commit()
        yield session


@pytest.fixture(autouse=True)
def mock_settings():
    mock = MagicMock()
    mock.SECRET_KEY = "test-secret"
    mock.ACCESS_TOKEN_EXPIRE_MINUTES = 30
    mock.FIRST_SUPERUSER = "admin@test.com"
    mock.FIRST_SUPERUSER_PASSWORD = "password-test"
    mock.FIRST_SUPERUSER_FIRSTNAME = "Admin"
    mock.FIRST_SUPERUSER_LASTNAME = "User"

    with patch("src.app.core.security.get_settings", return_value=mock):
        get_settings.cache_clear()
        yield mock
        get_settings.cache_clear()


@pytest.fixture
def superuser_token(mock_settings):
    access_token = create_access_token(
        subject=1,  # superuser id
        expires_delta=timedelta(minutes=mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return access_token


@pytest.fixture
def regular_token(mock_settings):
    access_token = create_access_token(
        subject=2,  # regular user id
        expires_delta=timedelta(minutes=mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return access_token


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

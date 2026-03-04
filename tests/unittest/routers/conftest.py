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

from typing import Any

from pydantic import EmailStr
from sqlmodel import Session, select

from src.app.core.security import DUMMY_HASH, get_password_hash, verify_password
from src.app.schemas.user import User, UserCreate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserCreate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def get_user_by_id(*, session: Session, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    session_user = session.exec(statement).first()
    return session_user


def authenticate_user(*, session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session=session, email=email)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_all_users(*, session: Session, offset: int = 0, limit: int = 100) -> list[User]:
    statement = select(User).offset(offset).limit(limit)
    users = session.exec(statement).all()
    return users


def delete_user(*, session: Session, email: EmailStr) -> bool:
    user = get_user_by_email(session=session, email=email)
    session.delete(user)
    session.commit()

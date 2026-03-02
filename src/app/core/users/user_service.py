from typing import Any

from pydantic import EmailStr
from sqlmodel import Session
from fastapi import HTTPException, status
from src.app.core.security import get_password_hash, verify_password
from src.app.schemas.user import (
    UpdatePassword,
    User,
    UserCreate,
    UserRegister,
    UserUpdate,
    UserUpdateMe,
)
from src.app.core.users import crud_users


def update_user_me(session: Session, user_in: UserUpdateMe, current_user: User) -> Any:
    if user_in.email:
        existing_user = crud_users.get_user_by_email(
            session=session, email=user_in.email
        )
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


def update_password_me(
    session: Session, body: UpdatePassword, current_user: User
) -> Any:

    verified, _ = verify_password(body.current_password, current_user.hashed_password)
    if not verified:
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()


def delete_me(session: Session, current_user: User):
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    session.delete(current_user)
    session.commit()


def get_all_users(session: Session, offset: int, limit: int) -> list[User]:
    return crud_users.get_all_users(session=session, offset=offset, limit=limit)


def get_user(session: Session, user_id: int, email: str) -> User:
    if user_id is not None:
        user = crud_users.get_user_by_id(session=session, user_id=user_id)
    elif email is not None:
        user = crud_users.get_user_by_email(session=session, email=email)
    else:
        raise HTTPException(status_code=400, detail="user_id or email must be provided")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(session: Session, user_create: UserCreate) -> User:
    user = crud_users.get_user_by_email(session=session, email=user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system.",
        )
    user = crud_users.create_user(session=session, user_create=user_create)
    return user


def patch_user(session: Session, user_patch: UserUpdate, email: EmailStr) -> User:
    user = crud_users.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    user = crud_users.update_user(session=session, db_user=user, user_in=user_patch)
    return user


def delete_user(session: Session, email: EmailStr, current_user: User) -> Any:
    if current_user.email == email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="To delete your own account, use the endpoint DELETE /v1/users/me",
        )
    user = crud_users.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    crud_users.delete_user(session=session, email=email)
    return {"detail": "User deleted successfully."}


def delete_me(session, current_user: User) -> Any:
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    crud_users.delete_user(session=session, email=current_user.email)
    return {"detail": "User deleted successfully."}


def register_user(session: Session, user_in: UserRegister) -> User:
    user = crud_users.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = crud_users.create_user(session=session, user_create=user_create)
    return user

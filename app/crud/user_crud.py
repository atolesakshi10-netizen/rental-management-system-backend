from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate

from app.auth.security import (
    hash_password,
    verify_password
)


def create_user(
    db: Session,
    user: UserCreate
):

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = get_user_by_email(
        db,
        email
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user


def get_user_by_id(
    db: Session,
    user_id: int
):

    return db.query(User).filter(
        User.id == user_id
    ).first()


def get_all_users(
    db: Session
):

    return db.query(User).all()
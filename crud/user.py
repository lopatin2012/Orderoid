# crud/user.py
# type: ignore

from utils.auth import pwd_context

from sqlalchemy.orm import Session

import models
import schemas

def create_user (db: Session, user: schemas.UserCreate):
    """
    Создать пользователя.
    :param db:
    :param user:
    :return:
    """
    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    """
    Получить пользователя по имени.
    :param db:
    :param username:
    :return:
    """
    return db.query(models.User).filter(models.User.username == username).first()
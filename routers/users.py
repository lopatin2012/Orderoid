# routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserResponse
from crud.user import create_user, get_user_by_username
from utils.auth import create_access_token, verify_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация пользователя.
    :param user:
    :param db:
    :return:
    """
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Имя занято")

    db_user = create_user(db, user)

    return db_user

@router.post("/token")
def login(user: UserCreate, db: Session = Depends(get_db)):
    """
    Вход в систему.
    :param user:
    :param db:
    :return:
    """
    db_user = get_user_by_username(db, user.username)

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    access_token = create_access_token(data={"sub": db_user.username, "id": db_user.id})

    return {"access_token": access_token, "token_type": "bearer"}

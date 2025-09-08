# utils/auth.py

from datetime import datetime, timedelta

from jose import JWTError, jwt

from passlib.context import CryptContext

from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status as status_fast_api

from sqlalchemy.orm import Session

from crud.user import get_user_by_username
from database import get_db

SECRET_KEY = "59b9b3ad198bff6ae31ac1a7c8d6edcb85267171171d0da9641c518e0f553ef6" # Для боевого проекта использовать другой ключ!!!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def create_access_token(data: dict):
    """
    Создать токен доступа.
    :param data:
    :return:
    """

    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Получить/подтвердить (токен) текущего пользователя.
    :param token:
    :param db:
    :return:
    """
    # Возвращаем в случае исключения.
    credentials_exception = HTTPException(
        status_code=status_fast_api.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учётные данные!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)

    if user is None:
        raise credentials_exception

    return user

# utils/security.py

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Проверить пароль.
    :param plain_password:
    :param hashed_password:
    :return:
    """

    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Получить хеш пароля.
    :param password:
    :return:
    """

    return pwd_context.hash(password)

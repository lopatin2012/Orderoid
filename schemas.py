# schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    """
    Базовый класс пользователя.
    """
    username: str # Имя.
    email: str # Почта.

class UserCreate(UserBase):
    """
    Создание пользователя.
    """
    password: str # Пароль.

class UserResponse(UserBase):
    """
    Ответ пользователя.
    """
    id: int # Идентификатор.
    level: int # Уровень.
    experience: int # Опыт.

    model_config = ConfigDict(from_attributes=True)

class ItemBase(BaseModel):
    """
    Базовый класс предмета.
    """
    name: str # Название предмета.
    description: Optional[str] = None # Описание.

    model_config = ConfigDict(from_attributes=True)

class ItemCreate(ItemBase):
    """
    Создание предмета.
    """
    pass

class ItemResponse(ItemBase):
    """
    Информация о предмете.
    """
    id: int # Идентификатор.
    owner_id: int # Владелец предмета.

    model_config = ConfigDict(from_attributes=True)

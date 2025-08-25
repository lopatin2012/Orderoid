# routers/items.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import ItemCreate, ItemResponse
from utils.auth import oauth2_scheme

from database import get_db

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemResponse)
def add_item(item: ItemCreate, access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Добавить декодирование токена.
    """
    Добавить мне предмет.
    :param item:
    :param access_token:
    :param db:
    :return:
    """
    pass

@router.get("/", response_model=list[ItemResponse])
def my_items(access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Получить список моих предметов.
    :param access_token:
    :param db:
    :return:
    """
    pass
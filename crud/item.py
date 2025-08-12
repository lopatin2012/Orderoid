# crud/item.py

from utils.auth import pwd_context

from sqlalchemy.orm import Session

import models
import schemas

def create_item(db: Session, item: schemas.ItemCreate, owner_id: int):
    """
    Создать предмет.
    :param db:
    :param item:
    :param owner_id:
    :return:
    """
    db_item = models.Item(**item.model_dump(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items_by_owner(db: Session, owner_id: int):
    """
    Вернуть предметы по владельцу.
    :param db:
    :param owner_id:
    :return:
    """
    return db.query(models.Item).filter(models.Item.owner_id == owner_id).all()

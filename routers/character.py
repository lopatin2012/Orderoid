# routers/character.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from crud.character import equip_item, upgrade_character_attribute

router = APIRouter(prefix="/character", tags=["character"])

@router.post("/equip/{item_id}/{slot}")
def api_equip_item(item_id: int, slot: str, db: Session = Depends(get_db)):
    """
    Экипировать предмет.
    :param item_id:
    :param slot:
    :param db:
    :return:
    """
    user_id = 1  # временно. FIXME заменить на JWT
    equip_item(db, user_id, item_id, slot)
    return {"status": "equipped", "item_id": item_id, "slot": slot}

@router.post("/upgrade/{attribute}")
def api_upgrade_attribute(attribute: str, db: Session = Depends(get_db)):
    """
    Улучшение характеристики персонажа.
    :param attribute:
    :param db:
    :return:
    """

    user_id = 1 # Временно.
    return upgrade_character_attribute(attribute, user_id, db)
# crud/character.py

from sqlalchemy.orm import Session
from models import Character, Item
from fastapi import HTTPException

def equip_item(db: Session, user_id: int, item_id: int, slot: str):
    """
    Экипировать предмет.
    :param db:
    :param user_id:
    :param item_id:
    :param slot:
    :return:
    """
    character = db.query(Character).filter(Character.user_id == user_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    item = db.query(Item).filter(Item.id == item_id, Item.owner_id == user_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Предмет не найден или не принадлежит вам")

    # Проверка, можно ли надеть FIXME доработать. Больше колец и артефакт.
    allowed_slots = {
        "artefact": ["artefact"],
        "head": ["head"],
        "body": ["body"],
        "legs": ["legs"],
        "gloves": ["gloves"],
        "ring": ["ring"],
        "feet": ["feet"],
        "weapon": ["weapon"],
    }

    if slot not in allowed_slots:
        raise HTTPException(status_code=400, detail="Недопустимый слот")

    slot_field = {
        "artefact": "artefact_item_id",
        "head": "head_item_id",
        "body": "body_item_id",
        "legs": "legs_item_id",
        "gloves": "gloves_item_id",
        "ring": "ring1_item_id",
        "feet": "feet_item_id",
        "weapon": "weapon_item_id",
    }[slot]

    setattr(character, slot_field, item.id)
    db.commit()
    db.refresh(character)
    return character
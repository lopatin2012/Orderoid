# crud/character.py

from fastapi import HTTPException
from sqlalchemy.orm import Session

from enums import EnumActionStatus, EnumNumbers, EnumAttributes

from models import Character, Item, User

from helpers.helper_character import get_result_calculate_upgrade_cost


def get_or_create_character(db: Session, user_id: int) -> Character:
    """
    Получить персонажа, или создать нового.
    :param db:
    :param user_id:
    :return:
    """
    character = db.query(Character).filter(Character.user_id == user_id).first()
    if not character:

        character = Character(
            user_id=user_id,
            endurance=EnumNumbers.ten.value,
            strength=EnumNumbers.ten.value,
            agility=EnumNumbers.ten.value,
            intelligence=EnumNumbers.ten.value,
            charisma=EnumNumbers.ten.value,
        )
        db.add(character)
        db.commit()
        db.refresh(character)

    return character

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

def upgrade_character_attribute(attribute: str, user_id: int, db: Session, value: int = 1):
    """
    Увеличить характеристику персонажа.
    :param db: Сессия БД.
    :param user_id: ID пользователя.
    :param attribute: Название атрибута: "strength", "agility" и т.д.
    :param value: На сколько увеличиваем.
    :return:
    """

    # Есть ли пользователь.
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")

    # Есть ли персонаж пользователя.
    character = db.query(Character).filter(Character.user_id == user_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден!")

    # Проверка существования атрибута.
    if attribute not in EnumAttributes.display_names():
        raise HTTPException(status_code=404, detail="Недопустимая характеристика!")

    # Сделать хитрый расчёт стоимости.
    cost = get_result_calculate_upgrade_cost(value)

    if user.experience < cost:
        raise HTTPException(
            status_code=400,
            detail=f"Недостаточно опыта. Требуется {cost}, у вас {user.experience}."
        )

    # Увеличиваем характеристику.
    current_value = getattr(character, attribute)
    setattr(character, attribute, current_value + value)

    # Вычитаем опыт.
    user.experience -= cost

    # Сохраняем изменения в БД.
    db.commit()
    db.refresh(character)
    db.refresh(user)

    return {
        "status": EnumActionStatus.success.value,
        "attribute": attribute,
        "new_value": current_value + value,
        "experience_left": user.experience,
    }

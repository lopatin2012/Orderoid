# routers/inventory.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from database import get_db

from models import User, Item, Character

router = APIRouter(tags=["inventory"])

templates = Jinja2Templates(directory="templates")

@router.get("/inventory", name="Инвентарь")
def view_inventory(request: Request, db: Session = Depends(get_db)):
    """
    Просмотр инвентаря.
    :param request:
    :param db:
    :return:
    """
    user_id: int = 1 # FIXME временно. Переделать на JWT.

    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    character = db.query(Character).filter(Character.user_id == user_id).first()

    # При отсутствии персонажа -> создаём.
    if not character:
        character = Character(user_id=user_id)
        db.add(character)
        db.commit()

    # Все предметы игрока.
    items = db.query(Item).filter(Item.owner_id == user_id).all()

    # Собираем слоты для проверки надетых вещей.
    equipped_ids = {
        character.artefact_item_id,
        character.head_item_id,
        character.body_item_id,
        character.legs_item_id,
        character.gloves_item_id,
        character.weapon_item_id,
        character.ring1_item_id,
        character.ring2_item_id,
        character.feet_item_id,
    }

    return templates.TemplateResponse(
        "inventory/main.html",
        {
            "request": request,
            "user": user,
            "items": items,
            "character": character,
            "equipped_ids": equipped_ids,
        }
    )
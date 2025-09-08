# routers/character.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from models import User, Item, Character, QuestProgress, BattleLog
from utils.auth import get_current_user
from database import get_db

from enums import EnumQuestStatus

from crud.character import equip_item, upgrade_character_attribute, get_or_create_character

router = APIRouter(prefix="/character", tags=["character"])

templates = Jinja2Templates(directory="templates")


@router.get("/", name="Профиль персонажа", response_model=None)
def view_character(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Просмотр персонажа.
    :param request:
    :param db:
    :param user:
    :return:
    """

    if not user:
         raise HTTPException(status_code=404, detail="Пользователь не найден")

    user_id = user.id

    character = get_or_create_character(db, user_id)
    inventory = db.query(Item).filter(Item.owner_id == user_id).all()

    # Активные задания.
    active_quests = (
        db.query(QuestProgress)
        .filter(
            QuestProgress.user_id == user_id,
            QuestProgress.status == EnumQuestStatus.active
        )
        .all()
    )

    # Последние бои.
    recent_battles = (
        db.query(BattleLog)
        .join(Character)
        .filter(Character.user_id == user_id)
        .order_by(BattleLog.ended_at.desc())
        .limit(5)
        .all()
    )

    return templates.TemplateResponse("character/profile.html", {
        "request": request,
        "user": user,
        "character": character,
        "inventory": inventory,
        "active_quests": active_quests,
        "recent_battles": recent_battles,
    })

@router.post("/equip/{item_id}/{slot}")
def api_equip_item(item_id: int, slot: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Экипировать предмет.
    :param item_id:
    :param slot:
    :param db:
    :param user:
    :return:
    """

    user_id = user.id
    equip_item(db, user_id, item_id, slot)

    return {"status": "equipped", "item_id": item_id, "slot": slot}

@router.post("/upgrade/{attribute}")
def api_upgrade_attribute(attribute: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Улучшение характеристики персонажа.
    :param attribute:
    :param db:
    :param user:
    :return:
    """

    user_id = user.id

    return upgrade_character_attribute(attribute, user_id, db)

# routers/minigame.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import User, Character

from config import ATTR_COST_MULTIPLIER
from enums import EnumActionStatus

router = APIRouter(prefix="/minigame", tags=["minigame"])
templates = Jinja2Templates(directory="templates")

class ClickerResult(BaseModel):
    clicks: int


@router.get("/clicker")
def play_clicker(request: Request, db: Session = Depends(get_db)):
    """
    Мини-игра: кликер.
    Необходимо сделать как можно больше кликов по движущейся цели.
    :param request:
    :param db:
    :return:
    """
    user_id = 1 # FIXME
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    character = db.query(Character).filter(Character.user_id == user_id).first()

    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    return templates.TemplateResponse(
        "minigame/clicker.html",
        {
            "request": request,
            "user": user,
            "character": character,
        }
    )

@router.post("/clicker/submit")
def submit_clicker_result(result: ClickerResult, db: Session = Depends(get_db)):
    """
    Выдать награду за количество кликов.
    :param result:
    :param db:
    :return:
    """
    user_id = 1 #FIXME
    user = db.query(User).get(user_id)

    calculate_min_exp_reward = 500 * user.level * ATTR_COST_MULTIPLIER

    exp_reward = min(result.clickes, calculate_min_exp_reward)
    user.experience += exp_reward
    db.commit()

    return {"status": EnumActionStatus.success.get_display_name(), "experience_gained": exp_reward}


# routers/quest.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from enums import EnumActionStatus

from utils.auth import get_current_user
from models import User
from crud.quest import start_quest, update_quest_progress, complete_quest_and_reward

router = APIRouter(prefix="/quests", tags=["quests"])

@router.post("/start/{quest_id}")
def api_start_quest(quest_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Начать задание.
    :param quest_id:
    :param db:
    :param user:
    :return:
    """

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user_id = user.id

    result = start_quest(db, user_id, quest_id)

    if not result:
        raise HTTPException(status_code=400, detail="Задание не существует!")

    return {"status": EnumActionStatus.success.value, "progress": result}

@router.post("/progress/{quest_id}")
def api_update_progress_quest(
        quest_id: int,
        amount: int = 1,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    """
    Обновить прогресс задания. Увеличить счётчик на 1.
    :param quest_id:
    :param amount:
    :param db:
    :param user:
    :return:
    """

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user_id = user.id

    result = update_quest_progress(db, user_id, quest_id, amount)

    if not result:
        raise HTTPException(status_code=400, detail="Задание не активно!")

    return {"status": EnumActionStatus.success.value, "progress": result.progress}

@router.post("/complete/{quest_id}")
def api_complete_quest(quest_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Завершить задание и получить награду.
    :param quest_id:
    :param db:
    :param user:
    :return:
    """

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user_id = user.id

    result = complete_quest_and_reward(db, user_id, quest_id)

    if not result:
        raise HTTPException(status_code=400, detail="Задание не активно!")

    return {"status": EnumActionStatus.success.value, "progress": result.progress}

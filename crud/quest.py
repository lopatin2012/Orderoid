# crud/quest.py

from datetime import datetime

from sqlalchemy.orm import Session
from models import Quest, QuestProgress, User, Item
from fastapi import HTTPException

from enums import EnumQuestStatus

def start_quest(db: Session, user_id: int, quest_id: int):
    """
    Активировать квест для персонажа.
    :param db:
    :param user_id:
    :param quest_id:
    :return:
    """

    quest = db.query(Quest).filter(Quest.id == quest_id).first()

    if not quest:
        raise HTTPException(status_code=404, detail="Задание не найдено!")

    # Проверяем прогресс.
    progress = db.query(QuestProgress).filter(
        QuestProgress.quest_id == quest_id,
        QuestProgress.user_id == user_id
    ).first()

    if progress:

        if progress.status == EnumQuestStatus.completed.value:
            raise HTTPException(status_code=400, detail="Квест уже выполнен!")

        elif progress.status == EnumQuestStatus.active.value:
            return progress

        else:
            progress.status = EnumQuestStatus.active.value
            progress.started_at = datetime.now()
            progress.progress = 0.0
    else:
        progress = QuestProgress(
            quest_id=quest_id,
            user_id=user_id,
            status=EnumQuestStatus.active.value,
            progress=0.0,
            need_value=0
        )
        db.add(progress)

    db.commit()
    db.refresh(progress)

    return progress

def update_quest_progress(db: Session, user_id: int, quest_id: int, amount: int = 1, current_conditions: dict = None):
    """
    Обновить прогресс задания.
    :param db:
    :param user_id:
    :param quest_id:
    :param current_conditions:
    :param amount:
    :return:
    """
    # FIXME подумать над реализацией обновления условий. Разные предметы/персонажи и т.д.

    if current_conditions is None:
        current_conditions = {"value": 0}

    progress = db.query(QuestProgress).filter(
        QuestProgress.quest_id == quest_id,
        QuestProgress.user_id == user_id,
        QuestProgress.status == EnumQuestStatus.active
    ).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Задание не найдено, либо не активно!")

    quest = progress.quest

    # Обновление условия.
    current_conditions = progress.current_conditions or current_conditions
    current = current_conditions.get("value", 0)
    new_value = current + amount

    # Ограничиваем прогресс
    if new_value > quest.target_count:
        new_value = quest.target_count

    current_conditions["value"] = new_value
    progress.current_conditions = current_conditions

    # Обновляем прогресс в процентах
    progress.progress = new_value / quest.target_count

    # Проверяем завершение
    if new_value >= quest.target_count:
        progress.status = EnumQuestStatus.completed
        progress.completed_at = datetime.now()

    db.commit()
    db.refresh(progress)

    return progress

def complete_quest_and_reward(db: Session, user_id: int, quest_id: int):
    """
    Завершение и награждение за выполнение задания.
    :param db:
    :param user_id:
    :param quest_id:
    :return:
    """

    progress = db.query(QuestProgress).filter(
        QuestProgress.quest_id == quest_id,
        QuestProgress.user_id == user_id,
        QuestProgress.status == EnumQuestStatus.completed
    ).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Задание не найдено или не завершено!")

    quest = progress.quest
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")

    # Награды
    rewards = {"experience": 0, "item": None}

    # Опыт
    if quest.reward_experience:
        user.experience += quest.reward_experience
        rewards["experience"] = quest.reward_experience

    # Предмет
    if quest.reward_item_id:
        # Добавляем предмет в инвентарь
        new_item = Item(
            name=quest.reward_item.name,
            description=quest.reward_item.description,
            owner_id=user_id,
            rarity=quest.reward_item.rarity,
            item_type=quest.reward_item.item_type,
            bonus_strength=quest.reward_item.bonus_strength,
            bonus_agility=quest.reward_item.bonus_agility,
            bonus_endurance=quest.reward_item.bonus_endurance,
            bonus_intelligence=quest.reward_item.bonus_intelligence,
            bonus_charisma=quest.reward_item.bonus_charisma,
            is_equippable=quest.reward_item.is_equippable
        )
        db.add(new_item)
        rewards["item"] = {"id": new_item.id, "name": new_item.name}

    db.commit()
    return {"status": EnumQuestStatus.completed, "rewards": rewards}

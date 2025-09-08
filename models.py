# models.py

from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime, Text,
    Float, JSON, UniqueConstraint, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

from enums import (
    EnumQuestStatus, EnumItemRarity, EnumItemType, EnumTypeEvent, EnumBuff, EnumTypeLocation,
    EnumMinigame, EnumNumbers, EnumNumbersFloat
)


class User(Base):
    """
    Пользователи.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)

    items = relationship("Item", back_populates="owner") # Предметы.
    skills = relationship("Skill", back_populates="user") # Способности.
    quest_progresses = relationship("QuestProgress", back_populates="user") # Прогресс задания.
    character = relationship("Character", uselist=False, back_populates="user") # Игровой персонаж.
    inventory = relationship("InventoryItem", back_populates="user")


class Character(Base):
    """
    Игровой персонаж.
    """
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Основные характеристики.
    strength = Column(Integer, default=EnumNumbers.ten.value) # Сила.
    agility = Column(Integer, default=EnumNumbers.ten.value) # Ловкость.
    endurance = Column(Integer, default=EnumNumbers.ten.value) # Выносливость.
    intelligence = Column(Integer, default=EnumNumbers.ten.value) # Интеллект.
    charisma = Column(Integer, default=EnumNumbers.ten.value) # Харизма

    # Экипировка (ссылки на предметы).
    artefact_item_id = Column(Integer, ForeignKey("items.id"), nullable=True) # Артефакт.
    head_item_id = Column(Integer, ForeignKey("items.id"), nullable=True) # Голова.
    body_item_id = Column(Integer, ForeignKey("items.id"), nullable=True) # Тело.
    legs_item_id = Column(Integer, ForeignKey("items.id"), nullable=True) # Ноги.
    gloves_item_id = Column(Integer, ForeignKey("items.id"), nullable=True) # Перчатки.
    weapon_item_id = Column(Integer, ForeignKey("items.id"), nullable=True) # Оружие.
    ring1_item_id = Column(Integer, ForeignKey("items.id"), nullable=True) # Кольцо 1.
    ring2_item_id = Column(Integer, ForeignKey("items.id"), nullable=True) # Кольцо 2.
    feet_item_id = Column(Integer, ForeignKey("items.id"), nullable=True) # Обувь.

    # Связи предметов.
    artefact_item = relationship("Item", foreign_keys=[artefact_item_id])
    head_item = relationship("Item", foreign_keys=[head_item_id])
    body_item = relationship("Item", foreign_keys=[body_item_id])
    legs_item = relationship("Item", foreign_keys=[legs_item_id])
    gloves_item = relationship("Item", foreign_keys=[gloves_item_id])
    weapon_item = relationship("Item", foreign_keys=[weapon_item_id])
    ring1_item = relationship("Item", foreign_keys=[ring1_item_id])
    ring2_item = relationship("Item", foreign_keys=[ring2_item_id])
    feet_item = relationship("Item", foreign_keys=[feet_item_id])

    user = relationship("User", back_populates="character")


class Item(Base):
    """
    Предметы.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)
    rarity = Column(SQLEnum(EnumItemRarity), default=EnumItemRarity.common)
    item_type = Column(SQLEnum(EnumItemType), nullable=False)
    # 'head', 'body', 'legs', 'gloves', 'ring 1', 'ring 2', 'feet', 'weapon'

    # Бонусы от предмета
    bonus_endurance = Column(Integer, default=0) # Выносливость.
    bonus_strength = Column(Integer, default=0) # Сила.
    bonus_agility = Column(Integer, default=0) # Ловкость.
    bonus_intelligence = Column(Integer, default=0) # Интеллект.
    bonus_charisma = Column(Integer, default=0) # Харизма.

    # Дополнительные параметры
    is_equippable = Column(Boolean, default=True)  # можно ли надеть
    is_equipped = Column(Boolean, default=False)  # надет ли прямо сейчас (альтернатива — через Character)

    owner = relationship("User", back_populates="items")


class InventoryItem(Base):
    """
    Предмет в инвентаре пользователя.
    """
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1) # Количество предмета. Стаки.
    acquired_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="inventory")
    item = relationship("Item")


class Skill(Base):
    """
    Способности.
    """
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    level = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    user = relationship("User", back_populates="skills")


class Enemy(Base):
    """
    Базовые противники.
    """
    __tablename__ = "enemies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    level = Column(Integer)
    health = Column(Integer)
    attack = Column(Integer)
    experience_reward = Column(Integer)
    loot_table = Column(JSON)  # список дропов: [{"item_id": 1, "chance": 0.5}, ...]


class Quest(Base):
    """
    Задания.
    """
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    target_count = Column(Integer)
    required_enemy_id = Column(Integer, ForeignKey("enemies.id"), nullable=True)
    reward_experience = Column(Integer, default=0)
    reward_item_id = Column(Integer, ForeignKey("items.id"), nullable=True)

    enemy = relationship("Enemy")
    reward_item = relationship("Item")
    progresses = relationship("QuestProgress", back_populates="quest")


class QuestProgress(Base):
    """
    Прогресс задания.
    """
    __tablename__ = "quest_progress"

    id = Column(Integer, primary_key=True)
    quest_id = Column(Integer, ForeignKey("quests.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    progress = Column(Float, default=0.0)  # От 0.0 до 1.0. Проценты выполнения.
    status = Column(SQLEnum(EnumQuestStatus), default=EnumQuestStatus.not_active)
    current_conditions = Column(JSON) # Необходимо количество для выполнения задания.
    started_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)

    quest = relationship("Quest", back_populates="progresses")
    user = relationship("User", back_populates="quest_progresses")

    __table_args__ = (UniqueConstraint("quest_id", "user_id"),)


class BattleLog(Base):
    """
    Журнал боёв.
    """
    __tablename__ = "battle_log"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    enemy_id = Column(Integer, ForeignKey("enemies.id"), nullable=False)

    # Результат боя.
    result = Column(String, nullable=False) # "Победа", "Поражение", "Ничья".

    # Урон и потери.
    damage_dealt = Column(Integer, default=0) # Нанесённый.
    damage_received = Column(Integer, default=0) # Полученный.
    items_used = Column(JSON, nullable=False) # Используемые предметы.
    # [{"item_id": 1, "name": "Зелье лечения", "count": 1}, ....]

    # Награды за бой.
    experience_gained = Column(Integer, default=0) # Опыт.
    gold_gained = Column(Integer, default=0) # Золото.
    items_dropped = Column(JSON, nullable=True) # Выпавшие предметы.
    # [{"item_id": 10, "name": "Крутой посох" "count": 1}, ....]

    # Время события.
    started_at = Column(DateTime, default=datetime.now)
    ended_at = Column(DateTime, default=datetime.now)

    # Связи между таблицами.
    character = relationship("Character")
    enemy = relationship("Enemy")

    def __str__(self):
        return f"Бой: {self.character.user.username} VS {self.enemy.name} -> {self.result}!"


class Location(Base):
    """
    Игровые локации.
    """
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(Text)
    image = Column(String) # Местоположение изображения.

    buff = Column(SQLEnum(EnumBuff), nullable=True) # Эффект на персонажа.
    event_type = Column(SQLEnum(EnumTypeEvent), nullable=True) # Тип локации.
    location_type = Column(SQLEnum(EnumTypeLocation), nullable=False, default=EnumTypeLocation.common) # Редкость локации.

    minigame = Column(SQLEnum(EnumMinigame), nullable=False, default=EnumMinigame.no_game) # Без игры.

    # Дополнительные параметры.
    difficulty = Column(Integer, default=EnumNumbers.one.value)  # сложность (1–10)
    experience_multiplier = Column(Float, default=EnumNumbersFloat.one.value)  # множитель опыта
    money_multiplier = Column(Float, default=EnumNumbersFloat.one.value)  # множитель валюты
    danger_level = Column(Integer, default=EnumNumbers.one.value)  # уровень угрозы (влияет на врагов)

    def __str__(self):
        return f"{self.name} ({self.location_type.dispay_name})"

    def __repr__(self):
        return f"<Location id={self.id} name='{self.name}' type={self.location_type.name}>"
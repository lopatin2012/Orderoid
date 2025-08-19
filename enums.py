from enum import Enum

class BaseEnum(Enum):
    """
    Базовый класс для всех enum в проекте.
    Автоматически:
    - устанавливает _value_ = имени элемента (например, 'common', 'head')
    - добавляет display_name и order
    - определяет __str__ и __repr__
    """

    def __init__(self, display_name: str, order: int):
        object.__setattr__(self, '_value_', self.name)
        self.display_name = display_name
        self.order = order

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"

    @classmethod
    def all(cls):
        """Возвращает все элементы enum."""
        return list(cls)

    @classmethod
    def names(cls):
        """Имена (ключы)."""
        return [e.name for e in cls]

    @classmethod
    def display_names(cls):
        """Отображаемые имена."""
        return [e.display_name for e in cls]

    def __lt__(self, other):
        """Сравнение по order."""
        if self.__class__ is other.__class__:
            return self.order < other.order
        return NotImplemented

class EnumQuestStatus(BaseEnum):
    not_active = ("Не активен", 1)
    active = ("Активный", 2)
    completed = ("Завершен", 3)
    failed = ("Провален", 4)

class EnumItemType(BaseEnum):
    artifact = ("Артефакт", 1)
    head = ("Голова", 2)
    body = ("Тело", 3)
    legs = ("Ноги", 4)
    gloves = ("Перчатки", 5)
    ring = ("Кольцо", 6)
    feet = ("Обувь", 7)
    weapon = ("Оружие", 8)
    shield = ("Щит", 9)
    potion = ("Зелье", 10)
    quest = ("Квестовый", 11)    # нельзя продать, только сдать.

class EnumItemRarity(BaseEnum):
    common = ("Обычный", 1)
    uncommon = ("Необычный", 2)
    rare = ("Редкий", 3)
    epic = ("Эпический", 4)
    legendary = ("Легендарный", 5)  # Лучший из всех предметов, даже донатных.
    donat = ("Купленный", 6)        # Можно купить за реальные деньги
    only_one = ("Единственный", 7)  # Уникальный предмет, один на сервер

    def color(self):
        """
        Цвет предмета.
        """
        return {
            "common": "#cccccc",
            "uncommon": "#1eff00",
            "rare": "#0070dd",
            "epic": "#a335ee",
            "legendary": "#ff8000",
            "donat": "#ff0000",
            "only_one": "#00ccff",
        }.get(self.name, "#ffffff")


class EnumBattleResults(BaseEnum):
    victory = ("Победа", 1)
    defeat = ("Поражение", 2)
    draw = ("Ничья", 3)


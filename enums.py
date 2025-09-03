# enums.py

from enum import Enum, IntEnum


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


    def get_display_name(self):
        """Возвращает отображаемое имя."""
        return self.display_name

    def get_order(self):
        """Получить номер."""
        return self.order

    @classmethod
    def all(cls):
        """Возвращает все элементы enum."""
        return list(cls)

    @classmethod
    def names(cls):
        """Имена (ключи)."""
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
    """
    Статус задания.
    """
    not_active = ("Не активен", 1)
    active = ("Активный", 2)
    completed = ("Завершен", 3)
    failed = ("Провален", 4)


class EnumActionStatus(BaseEnum):
    """
    Результат действия.
    """
    success = ("Успех", 1)
    failure = ("Провал", 2)


class EnumItemType(BaseEnum):
    """
    Тип предмета.
    """
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
    """
    Редкость предметов.
    """
    common = ("Обычный", 1) # +10%
    uncommon = ("Необычный", 2) # +25%
    rare = ("Редкий", 3) # +50%
    epic = ("Эпический", 4) # +80%
    legendary = ("Легендарный", 5)  # + 150%. Лучший из всех предметов, даже донатных.
    donat = ("Купленный", 6)        # + 100% Можно купить за реальные деньги.
    only_one = ("Единственный", 7)  # + 200% Уникальный предмет, один на сервер.

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
    """
    Результат сражений.
    """
    victory = ("Победа", 1)
    defeat = ("Поражение", 2)
    draw = ("Ничья", 3)


class EnumBuff(BaseEnum):
    """
    Бонусы для характеристик на игровом персонаже.
    """
    curiosity_boost = ("Увеличена общая скорость прокачки навыков!", 1)
    experience_boost = ("Увеличена скорость получения опыта!", 2)
    money_boost = ("Увеличено количество получаемой валюты!", 3)
    endurance_boost = ("Увеличена скорость прокачки выносливости!", 4)
    strength_boost = ("Увеличена скорость прокачки силы!", 5)
    agility_boost = ("Увеличена скорость прокачки ловкости!", 6)
    intelligence_boost = ("Увеличена скорость прокачки интеллекта!", 7)
    charisma_boost = ("Увеличена скорость прокачки харизмы!", 8)

    # Бонусы локации
    rest = ("Отдых", 41) # Восстановление характеристик.
    danger = ("Опасность", 42) # У врагов увеличен шанс попадания атаки по герою.
    search = ("Поиск", 43) # Увеличен шанс что-то/кого-то найти.

    # Особые.
    nothing = ("Ничего", 101) # Нет эффекта.


class EnumTypeEvent(BaseEnum):
    """
    Тип события.
    """
    positive_event = ("Положительное событие", 1)
    neutral_event = ("Нейтральное событие", 2)
    negative_event = ("Негативное событие", 3)


class EnumMinigame(BaseEnum):
    """
    Мини-игры.
    """
    no_game = ("Без игры", 1)
    clicker = ("Кликер", 2)
    cards = ("Карты", 3)
    race = ("Гонка", 4)
    reaction = ("Реакция", 5)
    memory_game = ("На память", 6)


class EnumNumbers(IntEnum):
    """
    Цифры. От 1 до 10.
    """
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10


class EnumNumbersFloat(Enum):
    """
    Цифры с точкой.
    """
    one = 1.0
    two = 2.0
    three = 3.0
    four = 4.0
    five = 5.0
    six = 6.0
    seven = 7.0
    eight = 8.0
    nine = 9.0
    ten = 10.0


class EnumEmploymentStatuses(BaseEnum):
    """
    Статусы занятости персонажа.
    """
    not_busy = ("not_busy", 1) # Персонаж ничем не занят.
    journey = ("journey", 2) # Путешествие.
    quest = ("quest", 3) # Задание.


class EnumTypeLocation(BaseEnum):
    """
    Тип редкости локации.
    """
    common = ("Обычная", 1)
    uncommon = ("Необычная", 2)
    rare = ("Редкая", 3)
    epic = ("Эпическая", 4)
    legendary = ("Легендарная", 5)

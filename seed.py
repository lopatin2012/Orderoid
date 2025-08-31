# seed.py

from sqlalchemy.orm import Session
from database import engine, Base
from models import Location, EnumBuff, EnumTypeEvent, EnumTypeLocation

# TODO. Добавить данные для других.
# Базовые локации.
INITIAL_LOCATIONS = [
    {
        "name": "Парк у озера",
        "description": "Спокойное место для прогулок. Можно встретить уток.",
        "image": "/static/images/locations/park.jpg",
        "buff": EnumBuff.rest.get_order(),
        "event_type": EnumTypeEvent.positive_event.get_order(),
        "location_type": EnumTypeLocation.common.get_order(),
        "minigame": None,
    },
    {
        "name": "Заброшенное здание",
        "description": "Темное и пугающее место. Кто знает, что внутри?",
        "image": "/static/images/locations/abandoned_building.jpg",
        "buff": EnumBuff.danger.get_order(),
        "event_type": EnumTypeEvent.negative_event.get_order(),
        "location_type": EnumTypeLocation.uncommon.get_order(),
        "minigame": "memory_game",
    },
    {
        "name": "Кофейня 'Уют'",
        "description": "Ароматный кофе и тёплая атмосфера.",
        "image": "/static/images/locations/cafe.jpg",
        "buff": EnumBuff.charisma_boost.get_order(),
        "event_type": EnumTypeEvent.positive_event.get_order(),
        "location_type": EnumTypeLocation.common.get_order(),
        "minigame": None,
    },
    {
        "name": "Городская площадь",
        "description": "Оживлённое место. Много людей, можно что-то найти.",
        "image": "/static/images/locations/square.jpg",
        "buff": EnumBuff.search.get_order(),
        "event_type": EnumTypeEvent.positive_event.get_order(),
        "location_type": EnumTypeLocation.uncommon.get_order(),
        "minigame": "clicker",
    },
]

def location_exists(db: Session, name: str) -> bool:
    """
    Проверить наличие локации в базе.
    :param db:
    :param name:
    :return:
    """
    return db.query(Location).filter(Location.name == name).first() is not None

def seed_locations(db: Session):
    """
    Добавить начальные локации, если их не было ранее в базе.
    :param db:
    :return:
    """
    for loc_data in INITIAL_LOCATIONS:
        if not location_exists(db, loc_data.get("name")):
            location = Location(**loc_data)
            db.add(location)
        else:
            print("Локация существует:", loc_data.get("name"))
    db.commit()

def main():
    """Создать таблицы с данными."""
    Base.metadata.create_all(bind=engine)

    # Открыть сессию
    from sqlalchemy.orm import sessionmaker
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()

    try:
        seed_locations(db) # Локации.
    finally:
        db.close()

if __name__ == "__main__":
    main()
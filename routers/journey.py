# routers/journey.py

from random import choice

from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from enums import EnumEmploymentStatuses

from database import get_db
from models import Location

router = APIRouter()

# Шаблоны.
templates = Jinja2Templates(directory="templates")

def __get_location_by_id(loc_id: int, db: Session) -> Location:
    """
    Получить последний id локации.
    :param db:
    :param loc_id:
    :return:
    """

    return db.query(Location).filter(Location.id == loc_id).first()

@router.get("/journey", name="Путешествие", response_model=None)
async def journey(request: Request, db: Session = Depends(get_db)):
    """
    Путешествие!
    :param request:
    :param db:
    :return:
    """
    path = request.session.get("path", [])
    current_index = request.session.get("current_index", 0)

    if not path:
        # Начинаем с первой локации.
        start_loc = choice(db.query(Location).all())
        path = [start_loc.id]
        current_index = 0
        request.session["state"] = EnumEmploymentStatuses.journey.get_display_name()
        request.session["path"] = path
        request.session["current_index"] = current_index

    current_loc_id = path[current_index]
    current_loc = __get_location_by_id(current_loc_id, db)

    return templates.TemplateResponse(
        "journey/main.html", {
            "request": request,
            "location": current_loc,
            "can_go_back": current_index > 0,
            "progress": f"{current_index + 1 / len(path)}",
        },
    )

@router.get("/journey/forward", response_model=None)
async def go_forward(request: Request, db: Session = Depends(get_db)):
    """
    Переместиться вперёд.
    :param request:
    :param db:
    :return:
    """
    path = request.session.get("path", [])
    current_index = request.session.get("current_index", 0)

    # Генерация новой локации.
    next_loc = choice(db.query(Location).all())
    path = path[:current_index + 1] # Обрезаем будущую локацию, если делали возвращение назад.
    path.append(next_loc.id)
    current_index += 1

    request.session["path"] = path
    request.session["current_index"] = current_index

    return RedirectResponse(url="/journey", status_code=303)

@router.get("/journey/back")
async def go_back(request: Request):
    """
    Вернуться назад.
    :param request:
    :return:
    """
    current_index = request.session.get("current_index", 0)
    if current_index > 0:
        request.session["current_index"] = current_index - 1
    return RedirectResponse(url="/journey", status_code=303)

@router.get("/journey/home")
async def go_home(request: Request):
    """
    Вернуться домой.
    Посчитать прогресс и зачислить бонусы за пройденные локации.
    :param request:
    :return:
    """
    path = request.session.get("path", [])
    levels_gained = len(path) * 10 # За каждую локацию начисляем 10 опыта. FIXME придумать иной расчёт.

    request.session.pop("path", None)
    request.session.pop("current_index", None)

    return templates.TemplateResponse(
        "journey/home.html",
        {
            "request": request,
            "levels_gained": levels_gained, # Переделать на опыт.
            "total_visited": len(path), # Количество всех посещений.
        }
    )

@router.get("/map", response_model=None)
async def show_map(request: Request, db: Session = Depends(get_db)):
    """
    Показать карту пройденных локаций.
    :param request:
    :param db:
    :return:
    """
    path = request.session.get("path", [])
    locations_list = [
        __get_location_by_id(loc_id, db) for loc_id in path
        if __get_location_by_id(loc_id, db) is not None
    ]
    return templates.TemplateResponse(
        "journey/map.html",
        {
            "request": request,
            "title": "Карта пройденных локаций",
            "locations_list": locations_list,
        }
    )

# routers/journey.py

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import random

from locations import LOCATIONS

router = APIRouter()

# Шаблоны.
templates = Jinja2Templates(directory="templates")

def get_location_by_id(loc_id: int):
    """
    Получить последний id локации.
    :param loc_id:
    :return:
    """
    return next((loc for loc in LOCATIONS if loc["id"] == loc_id), None)

@router.get("/journey", name="Путешествие")
async def journey(request: Request):
    """
    Путешествие!
    :param request:
    :return:
    """
    path = request.session.get("path", [])
    current_index = request.session.get("current_index", 0)

    if not path:
        # Начинаем с первой локации.
        start_loc = random.choice(LOCATIONS)
        path = [start_loc["id"]]
        current_index = 0
        request.session["path"] = path
        request.session["current_index"] = current_index

    current_loc_id = path[current_index]
    current_loc = get_location_by_id(current_loc_id)

    return templates.TemplateResponse(
        "journey/main.html", {
            "request": request,
            "location": current_loc,
            "can_go_back": current_index > 0,
            "progress": f"{current_index + 1 / len(path)}",
        },
    )

@router.get("/journey/forward")
async def go_forward(request: Request):
    """
    Переместиться вперёд.
    :param request:
    :return:
    """
    path = request.session.get("path", [])
    current_index = request.session.get("current_index", 0)

    # Генерация новой локации.
    next_loc = random.choice(LOCATIONS)
    path = path[:current_index + 1] # Обрезаем будущую локацию, если делали возвращение назад.
    path.append(next_loc["id"])
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

@router.get("/map")
async def show_map(request: Request):
    """
    Показать карту пройденных локаций.
    :param request:
    :return:
    """
    path = request.session.get("path", [])
    locations_list = [get_location_by_id(loc_id) for loc_id in path]
    return templates.TemplateResponse(
        "journey/map.html",
        {
            "request": request,
            "title": "Карта пройденных локаций",
            "locations_list": locations_list,
        }
    )
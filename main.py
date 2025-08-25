# main.py

import jinja2.exceptions
from fastapi import FastAPI

from fastapi.requests import Request

# База.

from database import engine, Base

from utils.auth import SECRET_KEY

# Роутеры.
from routers.users import router as router_users
from routers.items import router as router_items
from routers.journey import router as router_journey
from routers.character import router as router_character

# Статика и шаблоны.
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Middleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="Ordering")

# add SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Создание таблицы.
Base.metadata.create_all(bind=engine)

# Подключение роутеров.
app.include_router(router_users)
app.include_router(router_items)
app.include_router(router_journey)
app.include_router(router_character)

# Раздача статических файлов.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Шаблоны.
templates = Jinja2Templates(directory="templates")

# Стартовая страница.
@app.get("/")
def read_root(request: Request):
    try:
        template = templates.TemplateResponse(
            name="main/main.html",
            context={
                "request": request,
                # Заголовок страницы.
                "title": "Главная страница",
                # Сообщение о работе страницы.
                "message": "Страница загружена",

            }
        )
        return template
    except jinja2.exceptions.TemplateNotFound:
        return {"message": "Страница не найдена"}

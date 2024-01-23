"""Main application module use to run the app"""

from fastapi import FastAPI
from utils.database import engine, Base
from routes import menu, submenu, dish


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Alan Dzheliev's FastAPI CRUD App for Y_lab",
    summary="Standard CRUD endpoints for 3 entities: Menu, Submenu and Dish"
)

app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dish.router)

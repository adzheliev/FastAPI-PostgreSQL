from fastapi import FastAPI
from utils.database import engine, Base
from routes import menu, submenu, dish


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dish.router)

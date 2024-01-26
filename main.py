"""Main application module use to run the app"""

from fastapi import FastAPI
from utils.database import engine, Base
from routes import menu, submenu, dish
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Alan Dzheliev's FastAPI CRUD App for Y_lab",
    summary="Standard CRUD endpoints for 3 entities: Menu, Submenu and Dish"
)

app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dish.router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
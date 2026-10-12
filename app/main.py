from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.anime import anime_router
from app.routers.author import author_router
from app.routers.studio import studio_router

app = FastAPI()

STATIC_DIR = Path(__file__).resolve().parents[1] / 'static'
# Garante que a pasta exista antes de montar
STATIC_DIR.mkdir(exist_ok=True)
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')

app.include_router(anime_router)
app.include_router(author_router)
app.include_router(studio_router)

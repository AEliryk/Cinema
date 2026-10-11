import sys
from pathlib import Path

# Добавляем папку backend/ в sys.path, чтобы пакет app был виден
# независимо от того, откуда запускается файл
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.movies import router as movies_router
import uvicorn

app = FastAPI(
    title="Cinema — Каталог Фильмов",
    description="Cinema Backend API на FastAPI + SQLAlchemy + Alembic",
    version="1.0.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(categories_router, prefix="/categories", tags=["Категории"])
app.include_router(movies_router, prefix="/movies", tags=["Фильмы"])

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API каталога фильмов!"}



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
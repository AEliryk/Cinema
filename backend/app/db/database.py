from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.utils.config import settings
from typing import AsyncGenerator

# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(
    settings.get_db_url,
    echo=True, # Логируем SQL-запросы в консоль
)

# Фабрика асинхронных сессий
SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Зависимость для получения сессии базы данных в эндпоинтах
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

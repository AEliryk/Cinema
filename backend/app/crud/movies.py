from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from app.models.movies import Movie

async def create_movie(
    db: AsyncSession,
    title: str,
    description: str = None,
    release_year: int = None,
    rating: float = None,
    category_id: int = None
) -> Movie:
    # Создаем SQL-инструкцию вставки (insert) в стиле SQLAlchemy 2.0 с возвратом созданного объекта (returning)
    stmt = insert(Movie).values(
        title=title,
        description=description,
        release_year=release_year,
        rating=rating,
        category_id=category_id
    ).returning(Movie)
    # Выполняем асинхронную вставку в БД
    result = await db.execute(stmt)
    # Фиксируем изменения в базе данных
    await db.commit()
    # Извлекаем и возвращаем вставленный объект Movie
    return result.scalar_one()


async def get_movies(db: AsyncSession, category_id: int = None, skip: int = 0, limit: int = 100):
    # Создаем базовый SQL-запрос для выбора всех записей из таблицы Movie
    query = select(Movie)
    # Если передан фильтр по категории, добавляем условие фильтрации в запрос
    if category_id is not None:
        query = query.where(Movie.category_id == category_id)
    # Добавляем смещение (skip) и лимит (limit) к SQL-запросу для пагинации
    query = query.offset(skip).limit(limit)
    # Выполняем запрос асинхронно в базе данных
    result = await db.execute(query)
    # Возвращаем список объектов Movie с помощью scalars().all()
    return list(result.scalars().all())


async def get_movie_by_id(db: AsyncSession, movie_id: int):
    # Создаем SQL-запрос для выбора фильма по его ID (стиль SQLAlchemy 2.0)
    query = select(Movie).where(Movie.id == movie_id)
    # Выполняем асинхронный запрос в БД
    result = await db.execute(query)
    # Извлекаем и возвращаем первую найденную запись (или None, если ничего не найдено)
    return result.scalars().first()


async def update_movie(
    db: AsyncSession,
    movie_id: int,
    title: str = None,
    description: str = None,
    release_year: int = None,
    rating: float = None,
    category_id: int = None
):
    # Сначала находим существующий фильм по ID
    db_movie = await get_movie_by_id(db, movie_id)
    # Если фильм не найден, возвращаем None
    if not db_movie:
        return None
    
    # Обновляем название фильма, если было передано новое значение
    if title is not None:
        db_movie.title = title
    # Обновляем описание фильма, если было передано новое значение
    if description is not None:
        db_movie.description = description
    # Обновляем год выпуска, если было передано новое значение
    if release_year is not None:
        db_movie.release_year = release_year
    # Обновляем рейтинг, если было передано новое значение
    if rating is not None:
        db_movie.rating = rating
    # Обновляем ID категории, если было передано новое значение
    if category_id is not None:
        db_movie.category_id = category_id
        
    # Сохраняем изменения в базе данных
    await db.commit()
    # Обновляем состояние объекта из базы данных
    await db.refresh(db_movie)
    # Возвращаем обновленный объект фильма
    return db_movie


async def delete_movie(db: AsyncSession, movie_id: int):
    # Находим существующий фильм по ID
    db_movie = await get_movie_by_id(db, movie_id)
    # Если фильм не найден, возвращаем None
    if not db_movie:
        return None
        
    # Удаляем объект из сессии базы данных
    await db.delete(db_movie)
    # Фиксируем удаление в базе данных
    await db.commit()
    # Возвращаем удаленный объект фильма
    return db_movie


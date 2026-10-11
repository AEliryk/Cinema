from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.categories import Category


from sqlalchemy import insert

async def create_category(db: AsyncSession, name: str, description: str = None) -> Category:
    # Создаем SQL-инструкцию вставки (insert) в стиле SQLAlchemy 2.0 с возвратом созданного объекта (returning)
    stmt = insert(Category).values(name=name, description=description).returning(Category)
    # Выполняем асинхронную вставку в БД
    result = await db.execute(stmt)
    # Фиксируем изменения в базе данных
    await db.commit()
    # Извлекаем и возвращаем вставленный объект Category
    return result.scalar_one()


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # Создаем SQL-запрос для выбора всех записей из таблицы Category с поддержкой пагинации
    query = select(Category).offset(skip).limit(limit)
    # Выполняем запрос асинхронно в базе данных
    result = await db.execute(query)
    # Возвращаем список объектов Category с помощью scalars().all()
    return list(result.scalars().all())



async def get_category_by_id(db: AsyncSession, category_id: int):
    # Создаем SQL-запрос для выбора категории по её ID (стиль SQLAlchemy 2.0)
    query = select(Category).where(Category.id == category_id)
    # Выполняем асинхронный запрос в БД
    result = await db.execute(query)
    # Извлекаем и возвращаем первую найденную запись (или None, если ничего не найдено)
    return result.scalars().first()


async def update_category(db: AsyncSession, category_id: int, name: str = None, description: str = None):
    # Сначала находим существующую категорию по ID
    db_category = await get_category_by_id(db, category_id)
    if not db_category:
        return None
    
    # Обновляем поля, если были переданы новые значения
    if name is not None:
        db_category.name = name
    if description is not None:
        db_category.description = description
        
    # Сохраняем изменения в базе данных
    await db.commit()
    # Обновляем состояние объекта из базы данных
    await db.refresh(db_category)
    return db_category


async def delete_category(db: AsyncSession, category_id: int):
    # Находим существующую категорию по ID
    db_category = await get_category_by_id(db, category_id)
    if not db_category:
        return None
        
    # Удаляем объект из сессии базы данных
    await db.delete(db_category)
    # Фиксируем удаление в базе данных
    await db.commit()
    # Возвращаем удаленный объект
    return db_category


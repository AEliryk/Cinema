from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.categories import CategoryCreate, CategoryUpdate, CategoryInDB
from app.crud import categories as crud_categories

router = APIRouter()

@router.post("/", response_model=CategoryInDB, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем CRUD на наличие категории с таким же названием, если это необходимо.
    # В модели name unique=True. Если возникнет ошибка БД, SQLAlchemy вызовет IntegrityError.
    # Для простоты и соответствия CRUD-интерфейсу вызываем асинхронный метод CRUD.
    try:
        return await crud_categories.create_category(db, name=category.name, description=category.description)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Категория с таким именем уже существует или переданы неверные данные."
        )

@router.get("/", response_model=List[CategoryInDB])
async def read_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud_categories.get_categories(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=CategoryInDB)
async def read_category(id: int, db: AsyncSession = Depends(get_db)):
    db_category = await crud_categories.get_category_by_id(db, category_id=id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена."
        )
    return db_category

@router.put("/{id}", response_model=CategoryInDB)
async def update_category(id: int, category: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    db_category = await crud_categories.update_category(
        db, category_id=id, name=category.name, description=category.description
    )
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена для обновления."
        )
    return db_category

@router.delete("/{id}", response_model=CategoryInDB)
async def delete_category(id: int, db: AsyncSession = Depends(get_db)):
    db_category = await crud_categories.delete_category(db, category_id=id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена для удаления."
        )
    return db_category

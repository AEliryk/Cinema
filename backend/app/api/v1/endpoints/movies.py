from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.database import get_db
from app.schemas.movies import MovieCreate, MovieUpdate, MovieInDB
from app.crud import movies as crud_movies

router = APIRouter()

@router.post("/", response_model=MovieInDB, status_code=status.HTTP_201_CREATED)
async def create_movie(movie: MovieCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud_movies.create_movie(
            db,
            title=movie.title,
            description=movie.description,
            release_year=movie.release_year,
            rating=movie.rating,
            category_id=movie.category_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Фильм с таким названием уже существует, указан неверный ID категории или переданы неверные данные."
        )

@router.get("/", response_model=List[MovieInDB])
async def read_movies(
    category_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud_movies.get_movies(db, category_id=category_id, skip=skip, limit=limit)

@router.get("/{id}", response_model=MovieInDB)
async def read_movie(id: int, db: AsyncSession = Depends(get_db)):
    db_movie = await crud_movies.get_movie_by_id(db, movie_id=id)
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фильм не найден."
        )
    return db_movie

@router.put("/{id}", response_model=MovieInDB)
async def update_movie(id: int, movie: MovieUpdate, db: AsyncSession = Depends(get_db)):
    db_movie = await crud_movies.update_movie(
        db,
        movie_id=id,
        title=movie.title,
        description=movie.description,
        release_year=movie.release_year,
        rating=movie.rating,
        category_id=movie.category_id
    )
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фильм не найден для обновления."
        )
    return db_movie

@router.delete("/{id}", response_model=MovieInDB)
async def delete_movie(id: int, db: AsyncSession = Depends(get_db)):
    db_movie = await crud_movies.delete_movie(db, movie_id=id)
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фильм не найден для удаления."
        )
    return db_movie

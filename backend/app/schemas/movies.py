from pydantic import BaseModel, ConfigDict
from typing import Optional

# Базовая схема фильма
class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    rating: Optional[float] = None
    category_id: Optional[int] = None

# Схема для создания фильма (клиент присылает данные)
class MovieCreate(MovieBase):
    pass

# Схема для обновления фильма (все поля опциональны)
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    release_year: Optional[int] = None
    rating: Optional[float] = None
    category_id: Optional[int] = None

# Схема для возврата данных из БД (включает id)
class MovieInDB(MovieBase):
    id: int

    # Настройка для работы с ORM SQLAlchemy (в Pydantic v2 используется model_config)
    model_config = ConfigDict(from_attributes=True)

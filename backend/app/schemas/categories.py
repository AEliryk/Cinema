from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

# Базовая схема, содержащая общие поля
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

# Схема для создания категории (клиент присылает данные)
class CategoryCreate(CategoryBase):
    name: str = Field(..., min_length=1, description="Название категории")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Название категории не может быть пустым")
        return v.strip()

# Схема для обновления категории (все поля опциональны)
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Название категории")
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("Название категории не может быть пустым")
            return v.strip()
        return v

# Схема для возврата данных из БД (включает id)
class CategoryInDB(CategoryBase):
    id: int
    
    # Настройка для работы с ORM SQLAlchemy (в Pydantic v2 используется model_config)
    model_config = ConfigDict(from_attributes=True)

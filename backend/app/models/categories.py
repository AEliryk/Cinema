from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
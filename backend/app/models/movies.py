from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Float, ForeignKey
from app.db.base import Base

class Movie(Base):
    __tablename__ = "movies"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    release_year: Mapped[int] = mapped_column(Integer, nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    
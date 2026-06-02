from sqlalchemy.orm import Mapped

from .base import Base

#модель таблицы для категорий
class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]
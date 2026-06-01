from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

#наша таблица с тасками на основе класса Base
class TaskORM(Base):
    #название таблицы
    __tablename__ = "tasks"
    #поля таблицы - id у нас праймари кей и он по умолчанию там есть
    #типизируем через Mapped
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
#----------------------------------------------
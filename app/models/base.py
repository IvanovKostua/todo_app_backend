from uuid import uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# класс, от которого мы будем наследоваться, в lifespan будут созданы все таблицы
# из моделей на основе этого класса (КОТОРЫХ ЕЩЕ НЕ СУЩЕСТВУЕТ), если существуют
# то не создаст
class Base(DeclarativeBase):
    # задаем праймари кей, будет первый солбец у всех таблиц на основе этого класса
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

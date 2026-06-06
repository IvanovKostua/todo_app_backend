from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategoryORM


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ТУТ ПРОИСХОДИТ ВСЯ РАБОТА С БД (САМЫЙ НИЗКОУРОВНЕВЫЙ МОДУЛЬ)!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class CategoryRepository:
    # инициализация, получение сессии, запись в локальную переменную
    def __init__(self, db: Session) -> None:
        self.db = db

    # получаем список CategoryORM (метод scalars возвращает список запрашиваемых
    # полей из таблицы), тут указана вся запись целиком, потому
    # он вернет список категорий
    def get_all(self) -> list[CategoryORM]:
        categories = self.db.scalars(select(CategoryORM)).all()
        return list(categories)

    # получаем объект CategoryORM (одна категория), по заданному id
    def get_by_id(self, category_id: str) -> CategoryORM | None:
        return self.db.get(CategoryORM, category_id)

    # тут записываем в переменную новую категорию, поля заполняем в соответствии с
    # переданными значениями записываем title а id у нас primary_key и в лямбда функции
    # создается по умолчанию для всех ORM, это буквально прописано в Base классе
    def create(self, name) -> CategoryORM:
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        return new_category

    # принимает категорию, удаляем ее из сессии, в дальнейшем коммитим
    # и она удаляется уже из БД
    def delete(self, CategoryORM) -> None:
        self.db.delete(CategoryORM)

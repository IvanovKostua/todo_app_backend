from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository

# from app.repositories.task import TaskRepository
from app.schemas.categories import Category, CategoryCreate, CategoryUpdate


# наш класс ошибки
class CategoryNotFound(Exception):
    """Категория не найдена в БД"""


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(self.db)

    def list_category(self) -> list[Category]:
        categories_orm = self.category_repository.get_all()
        return [Category.model_validate(category) for category in categories_orm]

    def create_category(self, payload: CategoryCreate) -> Category:
        category_orm = self.category_repository.create(name=payload.name)

        self.db.commit()

        return Category.model_validate(category_orm)

    def update_category(self, category_id: str, payload: CategoryUpdate) -> Category:
        category_for_update = self.category_repository.get_by_id(
            category_id=category_id
        )

        if not category_for_update:
            raise CategoryNotFound(f"Категоряи с id {category_id} не найдена")

        if category_for_update.name is not None:
            category_for_update.name = payload.name

        self.db.commit()
        return Category.model_validate(category_for_update)

    def delete_category(self, category_id: str) -> None:
        category_for_delete = self.category_repository.get_by_id(
            category_id=category_id
        )
        if not category_for_delete:
            raise CategoryNotFound(f"Категоряи с id {category_id} не найдена")

        self.category_repository.delete(category_for_delete)

        self.db.commit()

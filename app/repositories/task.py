from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import TaskORM


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ТУТ ПРОИСХОДИТ ВСЯ РАБОТА С БД (САМЫЙ НИЗКОУРОВНЕВЫЙ МОДУЛЬ)!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class TaskRepository:
    # инициализация, получение сессии, запись в локальную переменную
    def __init__(self, db: Session) -> None:
        self.db = db

    # получаем список TaskORM (метод scalars возвращает список запрашиваемых
    # полей из таблицы), тут указана вся запись целиком, потому он вернет список задач
    def get_all(self) -> list[TaskORM]:
        tasks = self.db.scalars(select(TaskORM)).all()
        return list(tasks)

    # получаем объект TaskORM (одна задача), по заданному task_id
    def get_by_id(self, task_id: str) -> TaskORM | None:
        return self.db.get(TaskORM, task_id)

    # тут записываем в переменную новую таску, поля заполняем в соответствии с
    # переданными значениями записываем title, completed в начале всегда false,
    # а id у нас primary_key и в лямбда функции создается
    # по умолчанию для всех ORM, это буквально прописано в Base классе
    def create(self, title) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        return new_task

    # принимает таску, удаляем ее из сессии, в дальнейшем коммитим
    # и она удаляется уже из БД
    def delete(self, TaskORM) -> None:
        self.db.delete(TaskORM)

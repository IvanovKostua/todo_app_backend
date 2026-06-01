from sqlalchemy.orm import Session
from app.repositories.task import TaskRepository
from app.schemas.task import Task, TaskCreate, TaskUpdate

#наш класс ошибки
class TaskNotFound(Exception):
    """Задача не найдена в БД"""

#КЛАСС ДЛЯ РАБОТЫ С МОДУЛЕМ repositories, который работает с БД
#commit-ы происходят тут, потому что сервис отправляет несколько запросов в БД и если бы
#это происходило в модуле repositories то сессия ///сбрасывалась///? бы
class TaskService:
    #инитим, подключаем конкретную сессию
    def __init__(self, db: Session) -> None:
        self.db=db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[Task]:
        #в этой переменной находится результат выполнения функции get_all - ЭТО ВСЕ ТАСКИ
        tasks_orm = self.task_repository.get_all()
        #возвращаем список таск схем, при помощи model_validate этот объект гарантированно валидный
        #но, чтобы это работало нам нужно прописать в нашей схеме model_config, чтобы она была словарем
        #потому что этот метод работает только со словарями
        return [Task.model_validate(task) for task in tasks_orm]

    #метод создания таски, возвращает созданную только что таску
    #передаем pydantic схему тела запроса для создания новой таски
    def create_task(self, payload: TaskCreate) -> Task:
        #вызываем метод create, в нем создается новая запись в сессии, все поля заполняются
        #так как по умолчанию completed=False, а if - primary кей и генерится по дефолту
        #передаем только тайтл
        task_orm = self.task_repository.create(title=payload.title)
        #комитим изменения в БД
        self.db.commit()
        #возвращаем новую таску с валидными значениями
        return Task.model_validate(task_orm)

    #метод обновления таски, получаем id таски от фронтенда и передаем тело запроса на обнову
    #возвращаем таску отредаченную
    def update_task(self, task_id: str, payload: TaskUpdate) -> Task:
        #получаем из БД таску по id через модуль repositories
        task_for_update = self.task_repository.get_by_id(task_id=task_id)
        #тут мы проверяем есть ли такая таска в БД
        if not task_for_update:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        #тут условия на проверку того, что нам передано что-то
        #если были внесены изменения хоть в одно поле, то оно меняется в сессии и потом комит в БД
        if payload.title is not None:
            task_for_update.title = payload.title
        if payload.completed is not None:
            task_for_update.completed = payload.completed
        #комит в БД
        self.db.commit()
        #возвращем обновленнуб БД в валидном виде, благодаря функции model_validate из Pydantic
        return Task.model_validate(task_for_update)
    
    #Удаляем таску из БД, поучаем ID, возвращаем удаленную таску
    def delete_task(self, task_id: str) -> Task:
        #получаем из БД нужную таску
        task_for_delete = self.task_repository.get_by_id(task_id=task_id)
        #если таски нет рэйзим ошибку
        if not task_for_delete:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        #вызываем метод удаления таски из репозитория (он не выполняет комит, все комиты тут)
        self.task_repository.delete(task_for_delete)
        #комит, чтобы обновить БД
        self.db.commit()
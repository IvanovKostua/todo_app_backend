from sqlalchemy.orm import Session
from app.repositories.task import TaskRepository
from app.schemas.task import Task, TaskCreate, TaskUpdate


class TaskNotFound(Exception):
    """Задача не найдена в БД"""


class TaskService:
    def __init__(self, db: Session) -> None:
        self.db=db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[Task]:
        tasks_orm = self.task_repository.get_all()
        return [Task.model_validate(task) for task in tasks_orm]

    def create_task(self, payload: TaskCreate) -> Task:
        task_orm = self.task_repository.create(title=payload.title)
        self.db.commit()
        return Task.model_validate(task_orm)

    def update_task(self, task_id: str, payload: TaskUpdate) -> Task:
        task_for_update = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_update:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        
        if payload.title is not None:
            task_for_update.title = payload.title
        if payload.completed is not None:
            task_for_update.completed = payload.completed

        self.db.commit()
        return Task.model_validate(task_for_update)
    
    def delete_task(self, task_id: str) -> Task:
        task_for_delete = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        
        self.task_repository.delete(task_for_delete)
        self.db.commit()
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.task import TaskNotFound, TaskService
from app.api.dependencies import get_task_service

#в этом файле описыватся все роуты

#создаем конкретный роутер под таски (для категорий надо создать второй)
task_router = APIRouter(prefix="/tasks", tags=["tasks"])

#прописываем конкретные роуты (в скобках уже не будет /tasks, потому что указали префикс)
# tags указан для групировки сваггером по этому тэгу
@task_router.get("")
def get_tasks(
    task_service: TaskService = Depends(get_task_service)
) -> list[Task]:
    #прокидываем все зависимости, получаем объект Service
    #тут вызываем метод для получения всех тасок, который вызывает аналогичный метод уже в repositories
    #а тот уже обращается к БД
    return task_service.list_tasks()

@task_router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate, 
    task_service: TaskService = Depends(get_task_service)
) -> Task:
    #тут получаем результат выполнения функции создания таски, аналогично там 
    # service->repository (слоистая архитектура - разделение ответственности и это все)
    return task_service.create_task(payload)

@task_router.patch("/{task_id}")
def update_task(
    task_id: str, 
    payload: TaskUpdate, 
    task_service: TaskService = Depends(get_task_service)
) -> Task:
    #меняет таску, если ее нет то рэйзим ошибку
    try:
        return task_service.update_task(task_id, payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service: TaskService = Depends(get_task_service)) -> None:
    #аналогично удаляем таску, если ее нет то ошибка
    try:
        return task_service.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

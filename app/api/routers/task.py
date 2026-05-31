from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.task import TaskNotFound, TaskService
from app.api.dependencies import get_task_service

router = APIRouter(prefix="/tasks")


@router.get("")
def get_tasks(
    task_service: TaskService = Depends(get_task_service)
) -> list[Task]:
    return task_service.list_tasks()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate, 
    task_service: TaskService = Depends(get_task_service)
) -> Task:
    return task_service.create_task(payload)

@router.patch("/{task_id}")
def update_task(
    task_id: str, 
    payload: TaskUpdate, 
    task_service: TaskService = Depends(get_task_service)
) -> Task:
    try:
        return task_service.update_task(task_id, payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service: TaskService = Depends(get_task_service)) -> None:
    try:
        return task_service.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

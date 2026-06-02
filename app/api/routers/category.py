from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.categories import Category, CategoryCreate, CategoryUpdate
from app.services.category import CategoryNotFound, CategoryService
from app.api.dependencies import get_category_service
#создаем конкретный роутер под таски (для категорий надо создать второй)
category_router = APIRouter(prefix="/categories", tags=["categories"])

@category_router.get("")
def get_category(
    category_service: CategoryService = Depends(get_category_service)
) -> list[Category]:
    return category_service.list_category()

@category_router.post("", status_code=status.HTTP_201_CREATED)
def post_category(
    payload: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
) -> Category:
    return category_service.create_category(payload)

@category_router.patch("/{category_id}")
def patch_category(
    payload: CategoryUpdate,
    category_id: str,
    category_service: CategoryService = Depends(get_category_service)
) -> Category:
        #меняет категорию, если ее нет то рэйзим ошибку
    try:
        return category_service.update_category(category_id, payload)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str, 
    category_service: CategoryService = Depends(get_category_service)
):
    try:
        return category_service.delete_category(category_id)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


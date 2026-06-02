from fastapi import FastAPI

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.models.base import Base
from app.db.session import engine

from app.api.routers.task import task_router
from app.api.routers.category import category_router

from app.core.config import get_settings #функция, возвращающая все настройки, в том числе cors_allow_origins

#получаю объект настроек, для того, чтобы корс пробросить
settings = get_settings() #возможно лучше просто импортировать settings из db.session



#используется асинхронный декоратор из базовой contextlib, позволяет в лайвспане задавать логику
#перед началом обработки запросов и после окончания (yield - граница)
@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine) #создаем все таблицы, если их нет в БД, если есть не создаем
    yield


app = FastAPI(lifespan=lifespan) #объект фастапи (само приложение)
app.include_router(router=task_router) #пробрасываем наш роутер для тасок
app.include_router(router=category_router)
     
#корс определяем, чтобы у fatapi было понимание, кто может подключаться и какие запросы, 
# с какими заголовкам отправлять нашему серверу (не рекомендуется ставиь в методс и хэдэр * на продакшне)
app.add_middleware(
    CORSMiddleware, 
    allow_origins = [
        settings.cors_allow_origins[0],
    ],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True,
)


# def category_orm_to_model(cat_orm: CategoryORM) -> Category:
#     return Category(id=cat_orm.id, name=cat_orm.name)



#------------------------------------------------------
#CATEGORIES

# @app.get("/categories")
# def get_categories(db: Session = Depends(get_db)):

#     category_from_db = db.scalars(select(CategoryORM)).all()
#     return [category_orm_to_model(cat) for cat in category_from_db] 

# @app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
# def post_categories(payload: CategoryCreate, db: Session = Depends(get_db)):
#     new_cat = CategoryORM(name=payload.name)
#     db.add(new_cat)
#     db.commit()

#     return category_orm_to_model(new_cat)



# @app.patch("/categories/{category_id}", response_model=Category)
# def category_update(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db)):
#     cat_for_update = db.get(CategoryORM, category_id)
#     if payload.name:
#         cat_for_update.name = payload.name

#     db.commit()
#     return cat_for_update
    

# @app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
# def category_delete(category_id: str, db: Session = Depends(get_db)) -> None:
    # cat_for_delete = db.get(CategoryORM, category_id)
    # db.delete(cat_for_delete)
    # db.commit()
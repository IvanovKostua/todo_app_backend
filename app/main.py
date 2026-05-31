from fastapi import FastAPI

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.models.base import Base
from app.db.session import engine

from app.api.routers.task import router as task_router

# class CategoryORM(Base):
#     __tablename__ = "categories"

#     name: Mapped[str]

@asynccontextmanager
async def lifespan(_: FastAPI):
    print("before")
    Base.metadata.create_all(bind=engine)
    print("after")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)
     
app.add_middleware(
    CORSMiddleware, 
    allow_origins = [
        "http://localhost:3000"
    ],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True,
)



# def task_orm_to_model(task_orm: TaskORM) -> Task: 
#     return Task(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)

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
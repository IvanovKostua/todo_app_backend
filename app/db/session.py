from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL) #ДВИЖОК
Sessionlocal = sessionmaker(bind=engine) #СОЗДАНИЕ СЕССИЙ ДЛЯ ПОДКЛЮЕНИЯ

def get_db():
    """Функция для инъекции сессии Базы Данных"""
    db=Sessionlocal()
    
    try:
        yield db
    finally:
        db.close()

    db.close()

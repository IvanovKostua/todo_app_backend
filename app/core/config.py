from dataclasses import dataclass

#класс для хранения данных, он создает автоматом методы для отображения объекта, сравнения разных 
# объектов и опционально другие методы, а также позволяет записывать все следующим образом:
@dataclass(frozen=True) #frozen - защита от дурака, чтобы поля объекта этого класса было нельзя менять
class Settings:
    DATABASE_URL: str
    cors_allow_origins: list[str]

#метод, которым мы получаем все значения объекта, созданного выше
def get_settings() -> Settings:
    return Settings(
        DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:25432/postgres",
        cors_allow_origins = ["http://localhost:3000"],
    )

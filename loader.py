import database
from database.db import engine

# Создаем таблицы в бд
database.models.Base.metadata.create_all(bind=engine)

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config_data import config
from database import crud, models
from database.db import engine

# Создаём бота
bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# Создаем таблицы в бд
models.Base.metadata.create_all(bind=engine)

# Загружаем мейн-вопросы
crud.table_main_question.load_main_questions()

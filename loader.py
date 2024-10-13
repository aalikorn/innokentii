from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyrogram import Client

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

api_id = 26770220
api_hash = "85be3e1a9b6ad7e4420a93caa17ae448"
app = Client("get_chat_id", api_id=config.API_ID, api_hash=config.API_HASH,
             bot_token=config.TOKEN, in_memory=False)

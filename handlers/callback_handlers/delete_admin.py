from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from database import crud


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='delete_admin', state='*')
async def add_admin(call: types.CallbackQuery, state: FSMContext):
	text = '''Выберите админа'''
	await bot.send_message()

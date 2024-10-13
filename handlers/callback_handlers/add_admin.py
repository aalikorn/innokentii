from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from database import crud


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='add_admin_start', state='*')
async def add_admin(call: types.CallbackQuery, state: FSMContext):
	# даем сайды
	await state.set_state(UserStates.add_admin)
	text = '''Введите юзернейм(алиес) админа через @\n(например @UInnokentiibot)'''
	await call.message.edit_text(text=text)

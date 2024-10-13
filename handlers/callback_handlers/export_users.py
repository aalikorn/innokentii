from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from utils.export_users import export_users

from database import crud
from states.user_states import UserStates


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='export_users', state='*')
async def send_users_xlsx_file(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
	file_path = export_users()
	try:
		with open(file_path, 'rb') as file:
			await bot.send_document(chat_id=call.from_user.id, document=file)
	except Exception as e:
		await bot.send_message(call.from_user.id, f"Произошла ошибка при отправке файла: {e}")


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='export_users_party', state='*')
async def send_users_party_xlsx_file(call: types.CallbackQuery, state: FSMContext):
	await state.set_state(UserStates.export_users_party)
	await call.message.delete()
	await bot.send_message(call.from_user.id, f"Напиши номер группы, данные пользователей которой надо выгрузить")

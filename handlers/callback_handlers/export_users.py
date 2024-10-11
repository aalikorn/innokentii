from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from utils.export_users import export_users


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='export_users', state='*')
async def send_users_xlsx_file(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
	file_path = export_users()
	try:
		with open(file_path, 'rb') as file:
			await bot.send_document(chat_id=call.from_user.id, document=file)
	except Exception as e:
		await bot.send_message(call.from_user.id, f"Произошла ошибка при отправке файла: {e}")

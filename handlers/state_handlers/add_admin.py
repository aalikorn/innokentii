from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
from pyrogram.errors.exceptions.bad_request_400 import UsernameInvalid, UsernameNotOccupied

from loader import bot, dp, app
from states.user_states import UserStates
from database import crud
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.add_admin)
async def add_admin(message: types.Message, state=FSMContext):
	username = message.text.strip()
	try:
		user = await app.get_users(username)
		if crud.table_admin.add_admin(user.id):
			crud.table_admin.add_admin(user.id)  # Telegram ID админа
			await state.set_state(UserStates.start)
			await bot.send_message(chat_id=message.from_user.id,
								   text='Новый админ успешно добавлен',
								   reply_markup=keyboards.inline.admin.admin_markup())
		else:
			await state.set_state(UserStates.start)
			await bot.send_message(chat_id=message.from_user.id,
								   text='Пользователь уже является админом',
								   reply_markup=keyboards.inline.admin.admin_markup())
	except UsernameInvalid as exc:
		await state.set_state(UserStates.add_admin)
		await bot.send_message(chat_id=message.from_user.id,
							   text=f'Введен некорректный юзернейм, попробуйте еще раз')
	except UsernameNotOccupied as exc:
		await state.set_state(UserStates.add_admin)
		await bot.send_message(chat_id=message.from_user.id,
							   text=f'Ошибка, пользователя с таким юзернеймом не существует, попробуйте еще раз')

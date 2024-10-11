from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
import re

from loader import bot, dp
from states.user_states import UserStates


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.wait_name)
async def save_name(message: types.Message, state=FSMContext):
	regex = r'[a-zA-Zа-яА-ЯёЁ]+\s[a-zA-Zа-яА-ЯёЁ]+\s[a-zA-Zа-яА-ЯёЁ]+'

	await bot.delete_message(message.from_user.id, message.message_id)
	await bot.delete_message(message.from_user.id, message.message_id - 1)
	if re.fullmatch(regex, message.text):  # ФИО написано правильно
		await state.update_data(user_name=message.text)
		await state.set_state(UserStates.wait_age)
		await bot.send_message(chat_id=message.from_user.id, text='Сколько тебе лет?')
	else:
		await bot.send_message(
			chat_id=message.from_user.id,
			text='Некорректный формат ввода. Напиши свой полное ФИО. Не используй никаких дополнительных символов.'
		)


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.wait_age)
async def save_age(message: types.Message, state=FSMContext):
	await bot.delete_message(message.from_user.id, message.message_id)
	await bot.delete_message(message.from_user.id, message.message_id - 1)
	if message.text.isdigit() and (0 < int(message.text) <= 150):  # Возраст указан правильно
		await state.update_data(user_age=int(message.text))
		await state.set_state(UserStates.wait_mail)
		await bot.send_message(chat_id=message.from_user.id, text='Отправь свою почту')
	else:
		await bot.send_message(message.from_user.id, text='Некорректный формат ввода. Напиши свой возраст')

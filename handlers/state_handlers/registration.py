from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
import re

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards


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


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.wait_mail)
async def save_user(message: types.Message, state=FSMContext):
	regex = r'^\S+@\S+\.\S+$'

	await bot.delete_message(message.from_user.id, message.message_id)
	await bot.delete_message(message.from_user.id, message.message_id - 1)
	if re.fullmatch(regex, message.text):
		await state.set_state(state=None)
		data = await state.get_data()
		full_name = data.get('user_name')
		age = data.get('user_age')
		crud.table_user.add_user(
			telegram_id=message.from_user.id,
			full_name=full_name,
			age=age,
			mail=message.text
		)
		await bot.send_message(
			message.from_user.id,
			text='Поздравляем, ты успешно зарегистрировался. Чтобы запустить квест нажми кнопку "Начать"',
			reply_markup=keyboards.inline.quest.start_quest()
		)
	else:
		await bot.send_message(message.from_user.id, text='Некорректный формат ввода. Напиши свою почту')

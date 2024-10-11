from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['start'], state='*')
async def start(message: types.Message, state=FSMContext):
	text = """Привет! Меня зовут Бот Иннокентий и я провожу
	интерактивные экскурсии по Университету Иннополис.
	Если ты хочешь поучаствовать, чтобы узнать много
	нового и интересного про УИ, нажми кнопку «Начать»"""

	await bot.send_message(
		message.from_user.id,
		text=text
	)

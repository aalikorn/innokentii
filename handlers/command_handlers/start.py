from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from database import crud
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['start'], state='*')
async def start(message: types.Message, state=FSMContext):
	user = crud.table_user.get_user(message.from_user.id)
	if user is not None:
		text = 'Чтобы запустить квест нажми кнопку "Начать".'
		await bot.send_message(
			message.from_user.id,
			text=text,
			reply_markup=keyboards.inline.quest.start_quest()
		)
	else:
		text = 'Привет! \n' \
			   'Меня зовут Бот Иннокентий и я провожу ' \
			   'интерактивные экскурсии по Университету Иннополис.\n' \
			   'Перед началом работы тебе нужно заполнить анкету.'
		await bot.send_message(
			message.from_user.id,
			text=text,
			reply_markup=keyboards.inline.registartion.start_registration()
		)

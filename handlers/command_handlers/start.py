from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

import keyboards

from config_data import config
from loader import bot, dp
from states.user_states import UserStates
from database import crud


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['start'], state='*')
async def start(message: types.Message, state=FSMContext):
	await state.set_state(UserStates.start)
	if message.from_user.id in config.SUPER_ADMINS:
		text = 'Выберите действие'
		await bot.send_message(message.from_user.id, text, reply_markup=keyboards.inline.admin.admin_markup())
	elif message.from_user.id in [i[0] for i in crud.table_admin.get_all()]:
		text = 'Выберите действие'

		await bot.send_message(
			message.from_user.id,
			text=text,
			reply_markup=keyboards.inline.admin_tour.admin_tour_markup()
		)
	elif crud.table_user.get_user(message.from_user.id):
		text = crud.table_main_question.get_main_question(1).content  # первый мейн

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

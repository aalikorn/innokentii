from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
import keyboards


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text='accept_personal_data_handling', state=UserStates.start)
async def send_invite_text(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
	text = 'Привет! \n' \
		   'Меня зовут Бот Иннокентий и я провожу ' \
		   'интерактивные экскурсии по Университету Иннополис.\n' \
		   'Перед началом работы тебе нужно заполнить анкету.'
	await bot.send_message(
		call.from_user.id,
		text=text,
		reply_markup=keyboards.inline.registartion.start_registration()
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='start_registration', state='*')
async def start_registration(call: types.CallbackQuery, state: FSMContext):
	await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
	await state.set_state(UserStates.wait_name)
	await bot.send_message(call.from_user.id, text='Отлично, напиши своё полное ФИО')

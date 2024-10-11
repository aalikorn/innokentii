from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='start_registration', state='*')
async def start_registration(call: types.CallbackQuery, state: FSMContext):
	await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
	await state.set_state(UserStates.wait_name)
	await bot.send_message(call.from_user.id, text='Отлично, напиши своё полное ФИО')

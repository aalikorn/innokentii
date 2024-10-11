from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='create_question', state='*')
async def add_question(call: types.CallbackQuery, state: FSMContext):
	await call.message.edit_text(text='Выберите группу',
								 reply_markup=keyboards.inline.manage_questions.choose_group_markup())


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='group', state='*')
async def ask_question_content(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
	await state.set_state(UserStates.content)
	await bot.send_message(call.from_user.id, text='Введите содержание вопроса')

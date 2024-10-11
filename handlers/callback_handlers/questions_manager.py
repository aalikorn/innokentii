from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='create_question', state='*')
async def add_question(call: types.CallbackQuery, state: FSMContext):
	await state.set_state(UserStates.create_question)
	await call.message.edit_text(text='Выберите группу',
								 reply_markup=keyboards.inline.manage_questions.choose_group_markup())


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='delete_question', state='*')
async def delete_question(call: types.CallbackQuery, state: FSMContext):
	await state.set_state(UserStates.delete_question)
	await call.message.edit_text(text='Выберите группу',
								 reply_markup=keyboards.inline.manage_questions.choose_group_markup())


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='group',
						   state=UserStates.create_question)
async def create_question(call: types.CallbackQuery, state: FSMContext):
	group_id = int(call.data.split(':')[1])
	await call.message.delete()
	await state.update_data(group_id=group_id)
	await state.set_state(UserStates.content)
	await bot.send_message(call.from_user.id, text='Введите содержание вопроса')


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='group',
						   state=UserStates.delete_question)
async def choose_question(call: types.CallbackQuery, state: FSMContext):
	group_id = int(call.data.split(':')[1])
	await state.update_data(group=group_id)
	await call.message.edit_text('Выберите вопрос',
								 reply_markup=keyboards.inline.manage_questions.choose_question_markup(group_id))


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='question',
						   state=UserStates.delete_question)
async def delete_question(call: types.CallbackQuery, state: FSMContext):
	question_id = int(call.data.split(':')[1])
	await state.set_state(UserStates.start)
	await call.message.delete()
	await bot.send_message(call.from_user.id, 'Вопрос удалён')
	crud.table_side_question.delete_question(question_id)

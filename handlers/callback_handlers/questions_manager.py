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
								 reply_markup=keyboards.inline.manage_questions.choose_main_question_markup())


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='delete_question', state='*')
async def choose_main_question(call: types.CallbackQuery, state: FSMContext):
	await state.set_state(UserStates.delete_question)
	await call.message.edit_text(text='Выберите группу',
								 reply_markup=keyboards.inline.manage_questions.choose_main_question_markup())


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='edit_question', state='*')
async def choose_main_question(call: types.CallbackQuery, state: FSMContext):
	await state.set_state(UserStates.edit_question)
	await call.message.edit_text(text='Выберите группу',
								 reply_markup=keyboards.inline.manage_questions.choose_main_question_markup())


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='main_question',
						   state=UserStates.create_question)
async def create_question(call: types.CallbackQuery, state: FSMContext):
	main_question_id = int(call.data.split(':')[1])
	await call.message.delete()
	await state.update_data(main_question_id=main_question_id)
	await state.set_state(UserStates.content)
	await bot.send_message(call.from_user.id, text='Введите содержание вопроса')


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='main_question',
						   state=UserStates.delete_question)
async def choose_question(call: types.CallbackQuery, state: FSMContext):
	main_question_id = int(call.data.split(':')[1])
	await state.update_data(main_question_id=main_question_id)
	await call.message.edit_text('Выберите вопрос',
								 reply_markup=keyboards.inline.manage_questions.choose_question_markup(
									 main_question_id))


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='main_question',
						   state=UserStates.edit_question)
async def choose_question(call: types.CallbackQuery, state: FSMContext):
	main_question_id = int(call.data.split(':')[1])
	await state.update_data(main_question_id=main_question_id)
	await call.message.edit_text('Выберите вопрос',
								 reply_markup=keyboards.inline.manage_questions.choose_question_markup(
									 main_question_id))


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='question',
						   state=UserStates.delete_question)
async def delete_question(call: types.CallbackQuery, state: FSMContext):
	question_id = int(call.data.split(':')[1])

	await state.set_state(UserStates.start)
	await call.message.delete()
	await bot.send_message(call.from_user.id, 'Вопрос удалён',
						   reply_markup=keyboards.inline.admin.admin_markup())
	crud.table_side_question.delete_question(question_id)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='question',
						   state=UserStates.edit_question)
async def edit_question(call: types.CallbackQuery, state: FSMContext):
	question_id = int(call.data.split(':')[1])
	await call.message.edit_text('Что отредактировать',
								 reply_markup=keyboards.inline.manage_questions.edit_question_markup(question_id))


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='edit_question_content',
						   state=UserStates.edit_question)
async def edit_question_content(call: types.CallbackQuery, state: FSMContext):
	question_id = int(call.data.split(':')[1])
	await state.update_data(question_id=question_id)
	await state.set_state(UserStates.edit_question_content)
	await call.message.delete()
	await bot.send_message(call.from_user.id, 'Введите новое содержание вопроса')


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='edit_question_answer',
						   state=UserStates.edit_question)
async def edit_question_answer(call: types.CallbackQuery, state: FSMContext):
	question_id = int(call.data.split(':')[1])
	await state.update_data(question_id=question_id)
	await state.set_state(UserStates.edit_question_answer)
	await call.message.delete()
	await bot.send_message(call.from_user.id, 'Введите новый правильный ответ')


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text_startswith='edit_question_right_response',
						   state=UserStates.edit_question)
async def edit_question_right_response(call: types.CallbackQuery, state: FSMContext):
	question_id = int(call.data.split(':')[1])
	await state.update_data(question_id=question_id)
	await state.set_state(UserStates.edit_question_right_response)
	await call.message.delete()
	await bot.send_message(call.from_user.id, 'Введите новое сообщение при правильном ответе')


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text_startswith='edit_question_wrong_response',
						   state=UserStates.edit_question)
async def edit_question_wrong_response(call: types.CallbackQuery, state: FSMContext):
	question_id = int(call.data.split(':')[1])
	await state.update_data(question_id=question_id)
	await call.message.delete()
	await state.set_state(UserStates.edit_question_wrong_response)
	await bot.send_message(call.from_user.id, 'Введите новое сообщение при неправильном ответе')

from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
import re

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'], state=UserStates.content)
async def save_content(message: types.Message, state=FSMContext):
	await state.update_data(content=message.text)
	await state.set_state(UserStates.answer)
	await bot.send_message(chat_id=message.from_user.id, text='Введите правильный ответ')


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'], state=UserStates.answer)
async def save_answer(message: types.Message, state=FSMContext):
	await state.update_data(answer=message.text)
	await state.set_state(UserStates.right_response)
	await bot.send_message(chat_id=message.from_user.id, text='Что должен отвечать бот при правильном ответе')


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.right_response)
async def save_right_response(message: types.Message, state=FSMContext):
	await state.update_data(right_response=message.text)
	await state.set_state(UserStates.wrong_response)
	await bot.send_message(chat_id=message.from_user.id, text='Что должен отвечать бот при неправильном ответе')


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.wrong_response)
async def save_question(message: types.Message, state=FSMContext):
	await state.set_state(state=None)

	data = await state.get_data()
	content = data.get('content')
	answer = data.get('answer')
	right_response = data.get('right_response')
	group_id = data.get('group_id')

	crud.table_side_question.create_question(
		content=content,
		answer=answer,
		right_response=right_response,
		wrong_response=message.text,
		group_id=group_id
	)

	await bot.send_message(chat_id=message.from_user.id, text='Добавлен новый вопрос')


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.edit_question_content)
async def edit_question_content(message: types.Message, state=FSMContext):
	data = await state.get_data()
	question_id = data.get('question_id')
	crud.table_side_question.edit_question(question_id=question_id, content=message.text)
	await bot.send_message(message.from_user.id, 'Данные обновлены')


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.edit_question_answer)
async def edit_question_answer(message: types.Message, state=FSMContext):
	data = await state.get_data()
	question_id = data.get('question_id')
	crud.table_side_question.edit_question(question_id=question_id, answer=message.text)
	await bot.send_message(message.from_user.id, 'Данные обновлены')


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.edit_question_right_response)
async def edit_question_right_response(message: types.Message, state=FSMContext):
	data = await state.get_data()
	question_id = data.get('question_id')
	crud.table_side_question.edit_question(question_id=question_id, right_response=message.text)
	await bot.send_message(message.from_user.id, 'Данные обновлены')


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.edit_question_wrong_response)
async def edit_question_wrong_response(message: types.Message, state=FSMContext):
	data = await state.get_data()
	question_id = data.get('question_id')
	crud.table_side_question.edit_question(question_id=question_id, wrong_response=message.text)
	await bot.send_message(message.from_user.id, 'Данные обновлены')

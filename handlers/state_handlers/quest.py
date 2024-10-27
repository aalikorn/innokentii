import random

from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from database import crud


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.main_question)
async def save_answer_main(message: types.Message, state=FSMContext):
	main_q_data = await state.get_data()
	main_q_id = main_q_data.get('main_q_id')
	main_question = crud.table_main_question.get_main_question(main_q_id)

	if main_question is None:
		rating = crud.table_user.get_user(telegram_id=message.from_user.id).rating
		max_res = crud.table_main_question.count_rows() + crud.table_side_question.count_rows()
		text = (
			'Поздравляю, ты прошел всю интерактивную экскурсию по Университету Иннополис! '
			f'Твой результат составил Твой результат составил - {rating} / {max_res}.\n'
			'Надеюсь, тебе понравился этот опыт и ты сохранишь стикеры со мной, белым барсом Иннокентием! '
			'Удачи)\nКстати, не забывай подписаться на канал Университета Иннополис! '
			'Там мы выкладываем новости на самые интересные темы, касающиеся нашего университета)'
			'\n\nhttps://t.me/universityinnopolis'
		)
		await state.set_state(UserStates.start)
		await bot.send_message(chat_id=message.from_user.id, text=text)
		return

	group_side_questions = main_q_data.get('group_side_questions')

	main_answers = main_question.answer.split(',')
	if message.text.lower() in main_answers:
		sticker = r'CAACAgIAAxkBAAEM9ndnDC1zOI9LrQp12370PZCpgne6NgAC7lsAAqF0YUgaQhPljxXUbjYE'
		user = crud.table_user.get_user(message.from_user.id)
		crud.table_user.increase_rating(user.user_id)
		text = main_question.right_response
	else:
		sticker = r'CAACAgIAAxkBAAEM9nlnDC12lZU6FHBtypJFTNDtApEv4wACoF0AAudhYEj1zh3ry0asDzYE'
		text = main_question.wrong_response

	await state.set_state(UserStates.side_question)
	await bot.send_sticker(message.from_user.id, sticker)
	await bot.send_message(chat_id=message.from_user.id, text=text)

	id = group_side_questions[0].id

	text = group_side_questions.pop(0).content
	await state.update_data(current_side_question_id=id, group_side_questions=group_side_questions)
	await bot.send_message(chat_id=message.from_user.id, text=text)


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.side_question)
async def validate_side_answer(message: types.Message, state=FSMContext):
	data = await state.get_data()
	main_q_id = data.get('main_q_id')
	group_side_questions = data.get('group_side_questions')
	current_side_question_id = data.get('current_side_question_id')

	side_question = crud.table_side_question.get_side_question(current_side_question_id)
	user = crud.table_user.get_user(message.from_user.id)

	answer = message.text
	side_answers = side_question.answer.split(',')
	if answer.lower() in side_answers:
		sticker = r'CAACAgIAAxkBAAEM9ndnDC1zOI9LrQp12370PZCpgne6NgAC7lsAAqF0YUgaQhPljxXUbjYE'
		crud.table_user.increase_rating(user.user_id)
		text = side_question.right_response
	else:
		sticker = r'CAACAgIAAxkBAAEM9nlnDC12lZU6FHBtypJFTNDtApEv4wACoF0AAudhYEj1zh3ry0asDzYE'
		text = side_question.wrong_response

	await bot.send_sticker(message.from_user.id, sticker)
	await bot.send_message(chat_id=message.from_user.id, text=text)

	if len(group_side_questions) > 0:
		id = group_side_questions[0].id

		text = group_side_questions.pop(0).content
		await state.update_data(current_side_question_id=id, group_side_questions=group_side_questions)
		await bot.send_message(chat_id=message.from_user.id, text=text)
	else:
		main_question = crud.table_main_question.get_main_question(main_q_id + 1)

		if main_question is None:
			rating = crud.table_user.get_user(telegram_id=message.from_user.id).rating
			max_res = crud.table_main_question.count_rows() + crud.table_side_question.count_rows()

			sticker = r'CAACAgIAAxkBAAEM9nNnDC1pz44_LA1y-VtDvfsvIlF_cQACPmIAAje6YEg1eDNeRIlU4jYE'
			await bot.send_sticker(message.from_user.id, sticker)
			text = (
				'Поздравляю, ты прошел всю интерактивную экскурсию по Университету Иннополис! '
				f'Твой результат составил Твой результат составил {rating} / {max_res}.\n'
				'Надеюсь, тебе понравился этот опыт и ты сохранишь стикеры со мной, белым барсом Иннокентием! '
				'Удачи)\nКстати, не забывай подписаться на канал Университета Иннополис! '
				'Там мы выкладываем новости на самые интересные темы, касающиеся нашего университета)'
				'\n\nhttps://t.me/universityinnopolis'
			)
			await state.set_state(UserStates.start)
			await bot.send_message(chat_id=message.from_user.id, text=text)
			return

		text = main_question.content

		sticker = r'CAACAgIAAxkBAAEM9nlnDC12lZU6FHBtypJFTNDtApEv4wACoF0AAudhYEj1zh3ry0asDzYE'
		await bot.send_sticker(message.from_user.id, sticker)

		await state.set_state(UserStates.main_question)

		group_side_questions = crud.table_side_question.get_questions(main_question_id=main_q_id + 1)
		await state.update_data(main_q_id=main_q_id + 1, group_side_questions=group_side_questions,
								current_side_question_id=group_side_questions[0].id)
		await bot.send_message(chat_id=message.from_user.id, text=text)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import crud


def manage_questions_markup():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton("Создать новый вопрос", callback_data='create_question')
	btn2 = InlineKeyboardButton("Удалить вопрос", callback_data='delete_question')
	btn3 = InlineKeyboardButton("Изменить вопрос", callback_data='edit_question')
	markup.row(btn1)
	markup.row(btn2, btn3)
	return markup


def create_question_markup():
	markup = InlineKeyboardMarkup()
	for group in crud.table_group.get_all():
		btn = InlineKeyboardButton(f"{group.id}. {group.short_name}", callback_data=f'add_question:{group.id}')
		markup.row(btn)
	return markup


def choose_group_markup():
	markup = InlineKeyboardMarkup()
	for group in crud.table_group.get_all():
		btn = InlineKeyboardButton(f"{group.id}. {group.short_name}", callback_data=f'group:{group.id}')
		markup.row(btn)
	return markup


def choose_question_markup(group_id: int):
	markup = InlineKeyboardMarkup()
	for i, question in enumerate(crud.table_side_question.get_questions(group_id=group_id), start=1):
		btn = InlineKeyboardButton(f'{i}. {question.content}', callback_data=f'question:{question.id}')
		markup.row(btn)
	return markup


def edit_question_markup(question_id):
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton("Содержание вопроса",
								callback_data=f'edit_question_content:{question_id}')
	btn2 = InlineKeyboardButton("Правильный ответ",
								callback_data=f'edit_question_answer:{question_id}')
	btn3 = InlineKeyboardButton("Сообщение после правильного ответа",
								callback_data=f'edit_question_right_response:{question_id}')
	btn4 = InlineKeyboardButton("Сообщение после неправильного ответа",
								callback_data=f'edit_question_wrong_response:{question_id}')
	markup.row(btn1)
	markup.row(btn2)
	markup.row(btn3)
	markup.row(btn4)
	return markup

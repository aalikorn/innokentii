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


def choose_group_markup():
	markup = InlineKeyboardMarkup()
	for group in crud.table_main_question.get_all():
		btn = InlineKeyboardButton(f"{group.id}. {group.short_name}", callback_data=f'group:{group.id}')
		markup.row(btn)
	return markup

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_markup():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton("Создать новый вопрос", callback_data='create_question')
	btn2 = InlineKeyboardButton("Удалить вопрос", callback_data='delete_question')
	btn3 = InlineKeyboardButton("Изменить вопрос", callback_data='edit_question')
	btn4 = InlineKeyboardButton("Выгрузить пользователей", callback_data='export_users')
	btn5 = InlineKeyboardButton("Добавить админа-экскурсовода", callback_data='add_admin_start')
	markup.row(btn5)
	markup.row(btn1)
	markup.row(btn2, btn3)
	markup.row(btn4)
	return markup

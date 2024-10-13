from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def accept_personal_data_handling_markup():
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton('Продолжить', callback_data='accept_personal_data_handling')
	markup.row(btn)
	return markup


def start_registration():
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton('👤 Заполнить анкету', callback_data='start_registration')
	markup.row(btn)
	return markup

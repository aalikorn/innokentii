from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_registration():
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton('👤 Заполнить анкету', callback_data='start_registration')
	markup.row(btn)
	return markup

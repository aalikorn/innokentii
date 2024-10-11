from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_quest():
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton('▶️ Начать', callback_data='start_quest')
	markup.row(btn)
	return markup

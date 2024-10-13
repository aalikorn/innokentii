from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_tour_markup():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Создать новую группу", callback_data='admin_tour_create_party')
    btn2 = InlineKeyboardButton("Выгрузить пользователей", callback_data='export_users_party')
    markup.row(btn1)
    markup.row(btn2)
    return markup

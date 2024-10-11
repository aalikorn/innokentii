from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def manage_questions_markup():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Создать новый вопрос", callback_data='create_question'),
        InlineKeyboardButton("Удалить вопрос", callback_data='delete_question'),
        InlineKeyboardButton("Изменить вопрос", callback_data='edit_question')
    )

    return keyboard

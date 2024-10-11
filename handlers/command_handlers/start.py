from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

import keyboards

from config_data import config
from loader import bot, dp
from states.user_states import UserStates
from database import crud


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['start'], state='*')
async def start(message: types.Message, state=FSMContext):
    await state.set_state(UserStates.start)
    if (message.from_user.id in config.ADMINS):
        text = """Выбери действие:"""
        await message.reply(text, reply_markup=keyboards.inline.manage_questions.manage_questions_markup())
    elif crud.table_user.get_user(message.from_user.id):
        text = 'Чтобы запустить квест нажми кнопку "Начать".'
        await bot.send_message(
            message.from_user.id,
            text=text,
            reply_markup=keyboards.inline.quest.start_quest()
        )
    else:
        text = 'Привет! \n' \
               'Меня зовут Бот Иннокентий и я провожу ' \
               'интерактивные экскурсии по Университету Иннополис.\n' \
               'Перед началом работы тебе нужно заполнить анкету.'
        await bot.send_message(
            message.from_user.id,
            text=text,
            reply_markup=keyboards.inline.registartion.start_registration()
        )

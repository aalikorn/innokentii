from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

import keyboards

from config_data import config
from loader import bot, dp
from states.user_states import UserStates


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['start'], state='*')
async def start(message: types.Message, state=FSMContext):
    await state.set_state(UserStates.content)
    user_id = message.from_user.id
    if (user_id in config.ADMINS):
        text = """Выбери действие:"""

        await message.reply(text, reply_markup=keyboards.inline.manage_questions.manage_questions_markup())
    else:
        text = """Привет! Меня зовут Бот Иннокентий и я провожу
		интерактивные экскурсии по Университету Иннополис.
		Если ты хочешь поучаствовать, чтобы узнать много
		нового и интересного про УИ, нажми кнопку «Начать»"""

        await bot.send_message(
            message.from_user.id,
            text=text
        )

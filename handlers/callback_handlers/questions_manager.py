from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='create_question', state='*')
async def add_question(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.content)
    await bot.send_message(call.from_user.id, text='Введи твой вопрос:')

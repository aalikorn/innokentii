from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='start_quest', state='*')
async def start_quest(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.main_question)
    await state.update_data(main_q_id=0)
    await bot.send_message(call.from_user.id, text=':')

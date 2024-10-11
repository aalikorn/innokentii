from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from database import crud


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='start_quest', state='*')
async def start_quest(call: types.CallbackQuery, state: FSMContext):
    # даем сайды
    await state.set_state(UserStates.side_question)
    group_side_questions = crud.table_side_question.get_questions(main_question_id=1)
    await state.update_data(main_q_id=1, group_side_questions=group_side_questions,
                            current_side_question_id=group_side_questions[0].id)
    text = group_side_questions.pop(0).content
    await call.message.edit_text(text=text)

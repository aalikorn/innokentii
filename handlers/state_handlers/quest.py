from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
import re

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'], state=UserStates.main_question)
async def save_answer_main(message: types.Message, state=FSMContext):
    main_q_data = await state.get_data()
    main_q_id = main_q_data.get('main_q_id')

    text = crud.table_main_question.get_main_question(main_q_id).content

    await state.update_data(main_q_id=main_q_id+1)
    await state.set_state(UserStates.side_question)
    await bot.send_message(chat_id=message.from_user.id, text=text)





# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'], state=UserStates.answer)
# async def save_answer(message: types.Message, state=FSMContext):
#     await state.update_data(answer=message.text)
#     await state.set_state(UserStates.right_response)
#     await bot.send_message(chat_id=message.from_user.id, text='Что должен отвечать бот при правильном ответе:')
#
#
# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
#                     state=UserStates.right_response)
# async def save_right_response(message: types.Message, state=FSMContext):
#     await state.update_data(right_response=message.text)
#     await state.set_state(UserStates.wrong_response)
#     await bot.send_message(chat_id=message.from_user.id, text='Что должен отвечать бот при неправильном ответе:')
#
#
# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
#                     state=UserStates.wrong_response)
# async def save_question(message: types.Message, state=FSMContext):
#     await state.update_data(wrong_response=message.text)
#     await state.set_state(state=None)
#
#     data = await state.get_data()
#     content = data.get('content')
#     answer = data.get('answer')
#     right_response = data.get('right_response')
#     crud.table_side_question.create_question(
#         content=content,
#         answer=answer,
#         right_response=right_response,
#         wrong_response=message.text
#     )
#
#     await bot.send_message(chat_id=message.from_user.id, text='Добавлен новый вопрос')
#

from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
import re

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
                    state=UserStates.main_question)
async def save_answer_main(message: types.Message, state=FSMContext):
    main_q_data = await state.get_data()
    main_q_id = main_q_data.get('main_q_id')

    main_question = crud.table_main_question.get_main_question(main_q_id)
    if main_question is None:
        rating = crud.table_user.get_user(telegram_id=message.from_user.id).rating
        text = ('Поздравляю, ты прошел всю интерактивную экскурсию по '
                'Университету Иннополис от команды «Маркеры»! '
                f'Твой результат составил - {rating} / MAX_RES. Надеюсь, тебе понравился этот опыт и ты сохранишь ' # TODO
                'стикеры со мной, белым барсом Иннокентием! Удачи)')
        await bot.send_message(chat_id=message.from_user.id, text=text)
        return

    group_side_questions = main_q_data.get('group_side_questions')
    current_side_question_id = main_q_data.get('current_side_question_id')

    right_answer = main_question.answer
    if message.text.lower() == right_answer:
        text = main_question.right_response
        # text = '''Правильно! Вот след'''
        # TODO
    else:
        text = main_question.wrong_response
        # text = f'''Неверно((( Правильный ответ - "{right_answer}"'''

    await state.set_state(UserStates.side_question)
    await bot.send_message(chat_id=message.from_user.id, text=text)

    id = group_side_questions[0].id

    text = group_side_questions.pop(0).content
    await state.update_data(current_side_question_id=id, group_side_questions=group_side_questions)
    await bot.send_message(chat_id=message.from_user.id, text=text)


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
                    state=UserStates.side_question)
async def validate_side_answer(message: types.Message, state=FSMContext):
    data = await state.get_data()
    main_q_id = data.get('main_q_id')
    group_side_questions = data.get('group_side_questions')
    current_side_question_id = data.get('current_side_question_id')

    side_question = crud.table_side_question.get_side_question(current_side_question_id)
    user = crud.table_user.get_user(message.from_user.id)

    answer = message.text
    if answer.lower() == side_question.answer:
        crud.table_user.increase_rating(user.user_id)
        text = side_question.right_response
    else:
        text = side_question.wrong_response

    await bot.send_message(chat_id=message.from_user.id, text=text)

    if len(group_side_questions) > 0:
        id = group_side_questions[0].id

        text = group_side_questions.pop(0).content
        await state.update_data(current_side_question_id=id, group_side_questions=group_side_questions)
        await bot.send_message(chat_id=message.from_user.id, text=text)
    else:
        main_question = crud.table_main_question.get_main_question(main_q_id+1)
        if main_question is None:
            rating = crud.table_user.get_user(telegram_id=message.from_user.id).rating
            text = ('Поздравляю, ты прошел всю интерактивную экскурсию по '
                    'Университету Иннополис от команды «Маркеры»! '
                    f'Твой результат составил - {rating} / MAX_RES. Надеюсь, тебе понравился этот опыт и ты сохранишь '  # TODO
                    'стикеры со мной, белым барсом Иннокентием! Удачи)')
            await bot.send_message(chat_id=message.from_user.id, text=text)
            return
        text = main_question.content

        await state.set_state(UserStates.main_question)

        group_side_questions = crud.table_side_question.get_questions(main_question_id=main_q_id + 1)
        await state.update_data(main_q_id=main_q_id + 1, group_side_questions=group_side_questions,
                                current_side_question_id=group_side_questions[0].id)
        await bot.send_message(chat_id=message.from_user.id, text=text)

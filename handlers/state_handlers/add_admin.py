from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp, app
from states.user_states import UserStates
from database import crud


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
                    state=UserStates.add_admin)
async def add_admin(message: types.Message, state=FSMContext):
    username = message.text.strip()
    try:
        user = await app.get_users(username)
        crud.table_admin.add_admin(user.id)  # Telegram ID админа
        await state.set_state(UserStates.start)
        await bot.send_message(chat_id=message.from_user.id,
                               text='Новый админ успешно добавлен')  # TODO норм текст сюда
    except Exception as e:
        await state.set_state(UserStates.add_admin)
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ошибка, пользователя с таким юзернеймом не существует, попробуйте еще раз')  # \n{str(e)}

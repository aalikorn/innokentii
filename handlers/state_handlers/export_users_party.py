from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
import re
from utils.export_users import export_users_party

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
                    state=UserStates.export_users_party)
async def send_users_party(message: types.Message, state=FSMContext):
    """делаем вывод в ексель"""
    party_id = message.text
    regex = r'^\d+_\d+$'

    admin_tour = crud.table_admin.get_admin(telegram_id=message.from_user.id)
    if re.fullmatch(regex, party_id):
        if party_id.split('_')[1] in admin_tour.party_id.split(',') and party_id.split('_')[0] == str(admin_tour.admin_id):
            await state.set_state(UserStates.start)
            file_path = export_users_party(party_id)
            try:
                with open(file_path, 'rb') as file:
                    await bot.send_document(chat_id=message.from_user.id, document=file)
                    await bot.send_message(
                        message.from_user.id,
                        text='Выберите действие',
                        reply_markup=keyboards.inline.admin_tour.admin_tour_markup()
                    )
            except Exception as e:
                await bot.send_message(message.from_user.id, f"Произошла ошибка при отправке файла: {e}")
        else:
            text = 'Неправильный номер группы. Попробуйте еще раз'
            await bot.send_message(message.from_user.id, text)
    else:
        text = 'Неправильный номер группы. Попробуйте еще раз'
        await bot.send_message(message.from_user.id, text)

from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

import keyboards

from loader import bot, dp
from database import crud


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='admin_tour_create_party', state='*')
async def add_party(call: types.CallbackQuery, state=FSMContext):
	await call.message.delete()
	curr_admin = crud.table_admin.get_admin(call.from_user.id)
	party_ids = curr_admin.party_id
	curr_party_id = str(int(party_ids.split(',')[-1]) + 1)
	crud.table_admin.add_party_id(curr_admin.telegram_id, curr_party_id)
	text = f'Вы успешно создали новую группу\nId группы - {curr_admin.admin_id}_{curr_party_id}'
	await bot.send_message(chat_id=call.from_user.id, text=text)
	await bot.send_message(
		call.from_user.id,
		text='Выберите действие',
		reply_markup=keyboards.inline.admin_tour.admin_tour_markup()
	)

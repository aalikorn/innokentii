import os

from openpyxl import Workbook

from database import crud


def export_users():
	workbook = Workbook()
	sheet = workbook.active
	sheet.title = "user"

	data = [['Фио', 'Возраст', 'Почта', 'Результат', 'Номер группы']]
	for user in crud.table_user.get_all():
		data.append([user.full_name, user.age, user.mail, user.rating, user.party_id])

	for row in data:
		sheet.append(row)

	base_dir = os.path.dirname(os.path.dirname(__file__))
	file_name = os.path.join(base_dir, 'utils', 'users.xlsx')
	workbook.save(file_name)
	return os.path.join(base_dir, file_name)


def export_users_party(party_id: str):
	workbook = Workbook()
	sheet = workbook.active
	sheet.title = "user"
	data = [['Фио', 'Возраст', 'Почта', 'Результат', 'Номер группы']]
	for user in crud.table_user.get_all_party(party_id):
		data.append([user.full_name, user.age, user.mail, user.rating, user.party_id])

	for row in data:
		sheet.append(row)

	base_dir = os.path.dirname(os.path.dirname(__file__))
	file_name = os.path.join(base_dir, 'utils', 'users.xlsx')
	workbook.save(file_name)
	return os.path.join(base_dir, file_name)

from database import db
from database import models


def get_all():
	session = db.SessionLocal()
	query = session.query(models.Admin.telegram_id)

	return query.all()


def get_admin(telegram_id: int):
	session = db.SessionLocal()
	query = session.query(models.Admin)

	return query.filter(models.Admin.telegram_id == telegram_id).one_or_none()


def add_admin(telegram_id: int):
	session = db.SessionLocal()
	admin_exists = bool(get_admin(telegram_id))
	if not admin_exists:
		admin = models.Admin(telegram_id=telegram_id, party_id='0')
		session.add(admin)
		session.commit()
		return True
	return False


def add_party_id(telegram_id: int, curr_party_id: str):
	session = db.SessionLocal()
	admin = session.query(models.Admin).filter(models.Admin.telegram_id == telegram_id).one_or_none()
	admin.party_id = admin.party_id.lstrip('0,') + ',' + curr_party_id
	session.add(admin)
	session.commit()


def check_party_admin_id(party_id: str):  # проверка существует ли группа
	admin_id, party_num = party_id.split('_')
	session = db.SessionLocal()
	query = session.query(models.Admin)

	admin = query.filter(models.Admin.admin_id == int(admin_id)).one_or_none()
	if admin is None:
		return False

	return party_num in admin.party_id.split(',')

from database import db
from database import models


def get_all():
	"""Получить все данные из таблицы User"""
	session = db.SessionLocal()
	query = session.query(models.User)

	data = query.filter().all()
	return data


def get_user(telegram_id: int):
	session = db.SessionLocal()
	query = session.query(models.User)
	return query.filter(models.User.telegram_id == telegram_id).one_or_none()

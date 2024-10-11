from database import db
from database import models


def get_all():
	"""Получить все данные из таблицы User"""
	session = db.SessionLocal()
	query = session.query(models.User)

	data = query.filter().all()
	return data

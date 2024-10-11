from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, VARCHAR, Date
from sqlalchemy.orm import relationship

from database.db import Base


class User(Base):
	"""Таблица для пользователей"""
	__tablename__ = 'User'

	user_id = Column(Integer, primary_key=True, unique=True, nullable=False)
	telegram_id = Column(Integer, unique=True, nullable=False)
	full_name = Column(String, nullable=False)
	age = Column(Integer, nullable=False)
	mail = Column(String, nullable=False)

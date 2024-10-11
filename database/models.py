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
	rating = Column(Integer, default=0)


class MainQuestion(Base):
	"""Таблица для главных тематических вопросов"""
	__tablename__ = 'MainQuestion'

	id = Column(Integer, unique=True, nullable=False, primary_key=True)
	short_name = Column(String, nullable=False)
	content = Column(String, nullable=False)
	answer = Column(String)
	right_response = Column(String)
	wrong_response = Column(String)


class SideQuestion(Base):
	"""Таблица для побочного вопроса"""
	__tablename__ = 'SideQuestion'

	id = Column(Integer, primary_key=True, unique=True, nullable=False)
	main_question_id = Column(Integer, nullable=False)
	content = Column(String, nullable=False)
	answer = Column(String, nullable=False)
	right_response = Column(String, nullable=False)
	wrong_response = Column(String, nullable=False)

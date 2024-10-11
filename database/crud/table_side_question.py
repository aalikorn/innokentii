from database import db
from database import models


def create_question(content: str, answer: str, right_response: str, wrong_response: str, group_id: int):
	session = db.SessionLocal()
	side_question = models.SideQuestion(
		content=content,
		answer=answer,
		right_response=right_response,
		wrong_response=wrong_response,
		group_id=group_id
	)
	session.add(side_question)
	session.commit()


def get_questions(group_id: int):
	session = db.SessionLocal()
	query = session.query(models.SideQuestion)
	return query.filter(models.SideQuestion.group_id == group_id).all()


def delete_question(question_id: int):
	session = db.SessionLocal()
	query = session.query(models.SideQuestion)
	query.filter(models.SideQuestion.id == question_id).delete()
	session.commit()

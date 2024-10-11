from database import db
from database import models


def create_question(content: str, answer: str, right_response: str, wrong_response: str):
    session = db.SessionLocal()
    side_question = models.SideQuestion(
        content=content,
        answer=answer,
        right_response=right_response,
        wrong_response=wrong_response,
        main_question_id=1
    )
    session.add(side_question)
    session.commit()

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


def add_user(telegram_id: int, full_name: str, age: int, mail: str):
    session = db.SessionLocal()
    user = models.User(
        telegram_id=telegram_id,
        full_name=full_name,
        age=age,
        mail=mail
    )
    session.add(user)
    session.commit()


def increase_rating(user_id: int):
    session = db.SessionLocal()
    query = session.query(models.User)
    query.filter(models.User.user_id == user_id).update(
        {models.User.rating: models.User.rating + 1}
    )
    session.commit()

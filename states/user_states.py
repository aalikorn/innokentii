from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    start = State()  # Начальное состояние
    wait_name = State()  # Ожидаем ФИО пользователя
    wait_age = State()  # Ожидаем возраст пользователя
    wait_mail = State()  # Ожидаем электронную почту пользователя

    # добавление вопроса
    content = State()  # Содержание вопроса
    answer = State()  # Ответ на вопрос
    right_response = State()  # Что бот пишет при правильном ответе
    wrong_response = State()  # Что бот пишет при неправильном ответе

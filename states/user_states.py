from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
	start = State()  # Начальное состояние
	wait_name = State()  # Ожидаем ФИО пользователя
	wait_age = State()  # Ожидаем возраст пользователя
	wait_mail = State()  # Ожидаем электронную почту пользователя

	# добавление вопроса
	create_question = State()
	content = State()  # Содержание вопроса
	answer = State()  # Ответ на вопрос
	right_response = State()  # Что бот пишет при правильном ответе
	wrong_response = State()  # Что бот пишет при неправильном ответе

	# Удаление вопроса
	delete_question = State()

	# Изменение вопроса
	edit_question = State()
	edit_question_content = State()
	edit_question_answer = State()
	edit_question_right_response = State()
	edit_question_wrong_response = State()

	# Начало квеста
	side_question = State()  # Побочные вопросы
	main_question = State()  # Главные вопросы
from aiogram.utils import executor

from loader import dp, app
import handlers  # noqa


if __name__ == '__main__':
	app.start()
	executor.start_polling(dp)

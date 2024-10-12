from aiogram.utils import executor

from loader import dp
import handlers  # noqa

if __name__ == '__main__':
	executor.start_polling(dp)

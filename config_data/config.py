import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
	exit('Добавьте файл .env')
else:
	load_dotenv()

TOKEN = os.getenv('TOKEN')

base_dir = os.path.dirname(os.path.dirname(__file__))
DATABASE_URL = 'sqlite:///' + os.path.join(base_dir, 'database', os.getenv('DATABASE_NAME'))

ADMINS = [int(telegram_id) for telegram_id in os.getenv('ADMINS').split(',') if telegram_id.isdigit()]

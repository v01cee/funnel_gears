import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))

# Настройки базы данных
DATABASE_PATH = os.getenv('DATABASE_PATH', 'bot.db')

# Настройки логирования
LOG_LEVEL = 'INFO'

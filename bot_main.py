"""Основной файл Telegram бота-воронки"""

import asyncio
import logging
from aiogram import Bot, Dispatcher

# Импорты из наших модулей
from config.settings import BOT_TOKEN, LOG_LEVEL
from database.database import init_db
from handlers.router import router
from funnel.funnel_logic import check_and_send_steps

# Настройка логирования
logging.basicConfig(level=getattr(logging, LOG_LEVEL))

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем роутер
dp.include_router(router)

async def main():
    """Главная функция запуска бота"""
    # Инициализируем базу данных
    init_db()
    
    # Запускаем проверку шагов воронки в фоне
    asyncio.create_task(check_and_send_steps(bot))
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
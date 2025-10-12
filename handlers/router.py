"""Главный роутер для всех хендлеров"""

from aiogram import Router
from .commands import commands_router
from .callbacks import callbacks_router
from .admin import admin_router
from .get_id import get_id_router
from .middleware import LoggingMiddleware

# Создаем главный роутер
router = Router()

# Подключаем middleware
router.message.middleware(LoggingMiddleware())
router.callback_query.middleware(LoggingMiddleware())

# Подключаем специализированные роутеры
router.include_router(commands_router)
router.include_router(callbacks_router)
router.include_router(admin_router)
router.include_router(get_id_router)

"""Роутер для команд бота"""

from aiogram import Router
from aiogram.filters import Command
from .start import cmd_start

# Создаем роутер для команд
commands_router = Router()

# Регистрируем команды
commands_router.message.register(cmd_start, Command("start"))

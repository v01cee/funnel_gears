"""Роутер для callback запросов"""

from aiogram import Router
from .pdf_handler import send_pdf_handler

# Создаем роутер для callback'ов
callbacks_router = Router()

# Регистрируем callback хендлеры
callbacks_router.callback_query.register(send_pdf_handler, lambda c: c.data == "get_pdf")

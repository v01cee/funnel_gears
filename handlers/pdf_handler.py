"""Обработчик для отправки PDF файла"""

import os
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def send_pdf_handler(callback_query: types.CallbackQuery):
    """Обработчик нажатия на кнопку 'Забрать PDF'"""
    try:
        # Путь к PDF файлу
        pdf_path = "/app/files/5_errors_bot_beginners.pdf"
        
        # Проверяем, существует ли файл
        if os.path.exists(pdf_path):
            # Отправляем PDF файл
            with open(pdf_path, 'rb') as pdf_file:
                await callback_query.bot.send_document(
                    chat_id=callback_query.from_user.id,
                    document=pdf_file,
                    caption="🎁 Ваш подарок готов!\n\n**«5 ошибок, из-за которых новички мучаются с ботами»**\n\nСохраните этот чек-лист и используйте при создании ботов!\n\n💡 Хотите научиться создавать таких ботов? Курс по aiogram 3:\nhttps://stepik.org/course/220554",
                    parse_mode="Markdown"
                )
            
            # Отвечаем на callback
            await callback_query.answer("PDF отправлен! Проверьте чат 📄")
        else:
            # Если файл не найден, отправляем сообщение
            await callback_query.answer("Файл временно недоступен. Попробуйте позже.", show_alert=True)
            
    except Exception as e:
        await callback_query.answer("Произошла ошибка при отправке файла.", show_alert=True)
        print(f"Ошибка при отправке PDF: {e}")


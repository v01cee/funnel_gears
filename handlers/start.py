"""Обработчик команды /start"""

import logging
from datetime import datetime, timedelta
from aiogram import types
from aiogram.types import FSInputFile
from database.database import SessionLocal
from database.models import User, UserStep
from funnel.messages import get_welcome_message

async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    user = message.from_user
    
    # Сохраняем пользователя в БД
    db = SessionLocal()
    try:
        # Проверяем, существует ли пользователь
        existing_user = db.query(User).filter(User.user_id == user.id).first()
        if not existing_user:
            new_user = User(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            db.add(new_user)
            db.commit()
            await message.answer(f"Привет, {user.first_name}! Вы успешно зарегистрированы!")
        else:
            await message.answer(f"С возвращением, {user.first_name}!")
    finally:
        db.close()
    
    # Отправляем приветственное сообщение
    welcome_text, _ = get_welcome_message()
    await message.answer(welcome_text, parse_mode="Markdown")
    
    # Отправляем PDF файл сразу
    try:
        pdf_file = FSInputFile('/app/files/5_errors_bot_beginners.pdf')
        await message.bot.send_document(
            chat_id=user.id,
            document=pdf_file,
            caption="🎁 Ваш подарок готов!\n\n*«5 ошибок, из-за которых новички мучаются с ботами»*\n\nСохраните этот чек-лист и используйте при создании ботов!\n\n💡 Хотите научиться создавать таких ботов? Курс по aiogram 3:\nhttps://stepik.org/course/220554",
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Ошибка при отправке PDF: {e}")
        await message.answer("Файл временно недоступен. Попробуйте позже.")
    
    # Создаем только первый шаг (через час от текущего момента) если его еще нет
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже шаг hour_letter для этого пользователя
        existing_step = db.query(UserStep).filter(
            UserStep.user_id == user.id,
            UserStep.step_name == 'hour_letter'
        ).first()
        
        if not existing_step:
            hour_letter_step = UserStep(
                user_id=user.id,
                step_name='hour_letter',
                scheduled_time=datetime.utcnow() + timedelta(hours=1)
            )
            db.add(hour_letter_step)
            db.commit()
            logging.info(f"Создан шаг hour_letter для пользователя {user.id}")
        else:
            logging.info(f"Шаг hour_letter уже существует для пользователя {user.id}")
    finally:
        db.close()

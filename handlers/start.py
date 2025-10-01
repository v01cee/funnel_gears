"""Обработчик команды /start"""

import logging
from datetime import datetime, timedelta
from aiogram import types
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
    
    # Отправляем первое письмо с полезной инструкцией (подарок)
    welcome_text, welcome_keyboard = get_welcome_message()
    await message.answer(welcome_text, reply_markup=welcome_keyboard)
    
    # Создаем только первый шаг (через час от текущего момента)
    db = SessionLocal()
    try:
        hour_letter_step = UserStep(
            user_id=user.id,
            step_name='hour_letter',
            scheduled_time=datetime.utcnow() + timedelta(hours=1)
        )
        db.add(hour_letter_step)
        db.commit()
        logging.info(f"Создан шаг hour_letter для пользователя {user.id}")
    finally:
        db.close()

"""Обработчик команды /start"""

import logging
from datetime import datetime, timedelta
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.database import SessionLocal
from database.models import User, UserStep
from config.funnel_timing import FUNNEL_DELAYS
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
    
    # Создаем инлайн-кнопку для получения чек-листа
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="5 ошибок новичка", callback_data="get_5_mistakes")]
    ])
    
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=keyboard)
    
    # Создаем только первый шаг (через час от текущего момента) если его еще нет
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже какие-либо шаги воронки для этого пользователя
        existing_steps = db.query(UserStep).filter(
            UserStep.user_id == user.id
        ).all()
        
        if not existing_steps:
            # Создаем первый шаг только если у пользователя вообще нет шагов воронки
            try:
                hour_letter_step = UserStep(
                    user_id=user.id,
                    step_name='hour_letter',
                    scheduled_time=datetime.utcnow() + FUNNEL_DELAYS['hour_letter']
                )
                db.add(hour_letter_step)
                db.commit()
                logging.info(f"Создан шаг hour_letter для пользователя {user.id}")
            except Exception as e:
                # Если произошла ошибка уникальности (шаг уже существует)
                db.rollback()
                logging.warning(f"Не удалось создать шаг hour_letter для пользователя {user.id}: {e}")
        else:
            logging.info(f"У пользователя {user.id} уже есть {len(existing_steps)} шагов воронки. Новые шаги не создаются.")
    finally:
        db.close()

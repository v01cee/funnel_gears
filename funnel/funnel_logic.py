"""Логика работы воронки"""

import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot
from database.database import SessionLocal
from database.models import User, UserStep
from .messages import (
    get_hour_letter_message, get_day_letter_message, get_quality_letter_message,
    get_two_days_letter_message, get_product2_letter_message, get_client_story_message,
    get_discount_offer_message, get_ready_kit_message, get_oto_discount_message,
    get_survey_message
)

async def check_and_send_steps(bot: Bot):
    """Проверка и отправка шагов воронки"""
    while True:
        try:
            db = SessionLocal()
            current_time = datetime.utcnow()
            
            # Получаем все неотправленные шаги, время которых наступило
            steps_to_send = db.query(UserStep).filter(
                UserStep.sent == False,
                UserStep.scheduled_time <= current_time
            ).all()
            
            for step in steps_to_send:
                # Получаем данные пользователя
                user = db.query(User).filter(User.user_id == step.user_id).first()
                if user:
                    # Дополнительная проверка: убеждаемся, что шаг еще не отправлен
                    if not step.sent:
                        await send_step_message(bot, step, user, db)
                        
                        # Отмечаем шаг как отправленный
                        step.sent = True
                        db.commit()
                        
                        logging.info(f"Отправлен шаг {step.step_name} пользователю {user.user_id}")
                    else:
                        logging.warning(f"Шаг {step.step_name} для пользователя {user.user_id} уже был отправлен, пропускаем")
            
            db.close()
            
        except Exception as e:
            logging.error(f"Ошибка при проверке шагов: {e}")
            if 'db' in locals():
                db.close()
        
        # Ждем 5 секунд перед следующей проверкой (для тестирования)
        await asyncio.sleep(5)

async def send_step_message(bot: Bot, step: UserStep, user: User, db):
    """Отправка сообщения для конкретного шага"""
    message_text = ""
    next_step_name = None
    next_step_delay = None
    
    if step.step_name == 'hour_letter':
        message_text = get_hour_letter_message(user.first_name)
        next_step_name = 'day_letter'
        next_step_delay = timedelta(minutes=1)  # Через 1 минуту для тестирования
        
    elif step.step_name == 'day_letter':
        message_text = get_day_letter_message(user.first_name)
        next_step_name = 'quality_letter'
        next_step_delay = timedelta(minutes=1)  # Через 1 минуту для тестирования
        
    elif step.step_name == 'quality_letter':
        message_text = get_quality_letter_message(user.first_name)
        next_step_name = 'two_days_letter'
        next_step_delay = timedelta(minutes=1)  # Через 1 минуту для тестирования
        
    elif step.step_name == 'two_days_letter':
        message_text = get_two_days_letter_message(user.first_name)
        next_step_name = 'product2_letter'
        next_step_delay = timedelta(minutes=1)  # Через 1 минуту для тестирования
        
    elif step.step_name == 'product2_letter':
        message_text = get_product2_letter_message(user.first_name)
        next_step_name = 'product2_letter2'
        next_step_delay = timedelta(minutes=1)  # Через 1 минуту для тестирования
        
    elif step.step_name == 'product2_letter2':
        message_text = get_product2_letter_message(user.first_name)  # Повторное сообщение о продукте
        next_step_name = 'client_story'
        next_step_delay = timedelta(minutes=1)  # Через 1 минуту для тестирования
        
    elif step.step_name == 'client_story':
        message_text = get_client_story_message(user.first_name)
        next_step_name = 'discount_offer'
        next_step_delay = timedelta(minutes=1)  # Через 1 минуту для тестирования
        
    elif step.step_name == 'discount_offer':
        message_text = get_discount_offer_message(user.first_name)
        next_step_name = 'ready_kit'
        next_step_delay = timedelta(minutes=1)  # Через 1 минуту для тестирования
        
    elif step.step_name == 'ready_kit':
        message_text = get_ready_kit_message(user.first_name)
        next_step_name = 'oto_discount'
        next_step_delay = timedelta(minutes=1)  # Через 1 минуту для тестирования
        
    elif step.step_name == 'oto_discount':
        message_text = get_oto_discount_message(user.first_name)
        next_step_name = 'survey'
        next_step_delay = timedelta(minutes=1)  # Через 1 минуту для тестирования
        
    elif step.step_name == 'survey':
        message_text = get_survey_message(user.first_name)
        # Последний шаг - следующий не создаем
    
    # Отправляем сообщение
    if message_text:
        await bot.send_message(step.user_id, message_text)
        # Задержка в 5 секунд между сообщениями
        await asyncio.sleep(5)
    
    # Создаем следующий шаг, если он есть
    if next_step_name and next_step_delay:
        # Проверяем, не существует ли уже такой шаг для этого пользователя
        existing_next_step = db.query(UserStep).filter(
            UserStep.user_id == user.user_id,
            UserStep.step_name == next_step_name
        ).first()
        
        if not existing_next_step:
            try:
                next_step = UserStep(
                    user_id=user.user_id,
                    step_name=next_step_name,
                    scheduled_time=datetime.utcnow() + next_step_delay
                )
                db.add(next_step)
                db.commit()
                logging.info(f"Создан следующий шаг {next_step_name} для пользователя {user.user_id}")
            except Exception as e:
                # Если произошла ошибка уникальности (шаг уже существует)
                db.rollback()
                logging.warning(f"Не удалось создать шаг {next_step_name} для пользователя {user.user_id}: {e}")
        else:
            logging.warning(f"Шаг {next_step_name} для пользователя {user.user_id} уже существует, пропускаем создание")

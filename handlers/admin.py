"""Админка для управления ботом"""

import logging
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.database import SessionLocal, engine
from database.models import Base, User, UserStep
from sqlalchemy import text
from config.settings import ADMIN_ID

# Создаем роутер для админки
admin_router = Router()

# Список админов
ADMIN_IDS = [ADMIN_ID] if ADMIN_ID else []

def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь админом"""
    return user_id in ADMIN_IDS

@admin_router.message(Command("admin"))
async def admin_panel(message: types.Message):
    """Главная панель админки"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав доступа к админке")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
            InlineKeyboardButton(text="🗑️ Пересоздать БД", callback_data="admin_recreate_db")
        ],
        [
            InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users"),
            InlineKeyboardButton(text="📝 Шаги воронки", callback_data="admin_steps")
        ],
        [
            InlineKeyboardButton(text="🚀 Запустить воронку", callback_data="admin_start_funnel"),
            InlineKeyboardButton(text="⏹️ Остановить воронку", callback_data="admin_stop_funnel")
        ]
    ])
    
    await message.answer(
        "🔧 **Панель администратора**\n\n"
        "Выберите действие:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@admin_router.callback_query(lambda c: c.data == "admin_stats")
async def show_stats(callback: types.CallbackQuery):
    """Показать статистику"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав доступа", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        # Общая статистика
        total_users = db.query(User).count()
        total_steps = db.query(UserStep).count()
        sent_steps = db.query(UserStep).filter(UserStep.sent == True).count()
        pending_steps = db.query(UserStep).filter(UserStep.sent == False).count()
        
        # Статистика по шагам
        steps_stats = db.query(
            UserStep.step_name,
            db.func.count(UserStep.id).label('count'),
            db.func.count(db.case([(UserStep.sent == True, 1)], else_=0)).label('sent_count')
        ).group_by(UserStep.step_name).all()
        
        stats_text = f"📊 **Статистика бота**\n\n"
        stats_text += f"👥 Всего пользователей: {total_users}\n"
        stats_text += f"📝 Всего шагов: {total_steps}\n"
        stats_text += f"✅ Отправлено: {sent_steps}\n"
        stats_text += f"⏳ Ожидает отправки: {pending_steps}\n\n"
        stats_text += f"📈 **По шагам:**\n"
        
        for step_name, count, sent_count in steps_stats:
            stats_text += f"• {step_name}: {sent_count}/{count}\n"
        
        await callback.message.edit_text(
            stats_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
            ])
        )
    finally:
        db.close()

@admin_router.callback_query(lambda c: c.data == "admin_recreate_db")
async def recreate_database(callback: types.CallbackQuery):
    """Пересоздать базу данных"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав доступа", show_alert=True)
        return
    
    try:
        # Удаляем все таблицы
        Base.metadata.drop_all(bind=engine)
        
        # Создаем таблицы заново
        Base.metadata.create_all(bind=engine)
        
        await callback.message.edit_text(
            "✅ **База данных успешно пересоздана!**\n\n"
            "Все данные удалены, таблицы созданы заново.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
            ])
        )
        
        logging.info("База данных пересоздана администратором")
        
    except Exception as e:
        await callback.message.edit_text(
            f"❌ **Ошибка при пересоздании БД:**\n\n{str(e)}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
            ])
        )
        logging.error(f"Ошибка при пересоздании БД: {e}")

@admin_router.callback_query(lambda c: c.data == "admin_users")
async def show_users(callback: types.CallbackQuery):
    """Показать список пользователей"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав доступа", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.created_at.desc()).limit(10).all()
        
        users_text = "👥 **Последние 10 пользователей:**\n\n"
        for user in users:
            username = f"@{user.username}" if user.username else "без username"
            users_text += f"• {user.first_name} ({username})\n"
            users_text += f"  ID: {user.user_id}\n"
            users_text += f"  Дата: {user.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        
        await callback.message.edit_text(
            users_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
            ])
        )
    finally:
        db.close()

@admin_router.callback_query(lambda c: c.data == "admin_steps")
async def show_steps(callback: types.CallbackQuery):
    """Показать шаги воронки"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав доступа", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        steps = db.query(UserStep).order_by(UserStep.created_at.desc()).limit(20).all()
        
        steps_text = "📝 **Последние 20 шагов воронки:**\n\n"
        for step in steps:
            status = "✅" if step.sent else "⏳"
            steps_text += f"{status} {step.step_name}\n"
            steps_text += f"  Пользователь: {step.user_id}\n"
            steps_text += f"  Время: {step.scheduled_time.strftime('%d.%m.%Y %H:%M')}\n\n"
        
        await callback.message.edit_text(
            steps_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
            ])
        )
    finally:
        db.close()

@admin_router.callback_query(lambda c: c.data == "admin_start_funnel")
async def start_funnel_for_all(callback: types.CallbackQuery):
    """Запустить воронку для всех пользователей"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав доступа", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        from datetime import datetime, timedelta
        
        # Получаем всех пользователей без шагов воронки
        users_without_steps = db.query(User).filter(
            ~User.user_id.in_(
                db.query(UserStep.user_id).distinct()
            )
        ).all()
        
        created_count = 0
        for user in users_without_steps:
            try:
                hour_letter_step = UserStep(
                    user_id=user.user_id,
                    step_name='hour_letter',
                    scheduled_time=datetime.utcnow() + timedelta(days=1)  # Через день
                )
                db.add(hour_letter_step)
                created_count += 1
            except Exception as e:
                logging.warning(f"Не удалось создать шаг для пользователя {user.user_id}: {e}")
        
        db.commit()
        
        await callback.message.edit_text(
            f"🚀 **Воронка запущена!**\n\n"
            f"Создано шагов: {created_count}\n"
            f"Пользователей обработано: {len(users_without_steps)}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
            ])
        )
    finally:
        db.close()

@admin_router.callback_query(lambda c: c.data == "admin_stop_funnel")
async def stop_funnel(callback: types.CallbackQuery):
    """Остановить воронку (удалить все неотправленные шаги)"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав доступа", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        # Удаляем все неотправленные шаги
        deleted_count = db.query(UserStep).filter(UserStep.sent == False).delete()
        db.commit()
        
        await callback.message.edit_text(
            f"⏹️ **Воронка остановлена!**\n\n"
            f"Удалено неотправленных шагов: {deleted_count}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
            ])
        )
    finally:
        db.close()

@admin_router.callback_query(lambda c: c.data == "admin_back")
async def back_to_admin(callback: types.CallbackQuery):
    """Вернуться в главное меню админки"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав доступа", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
            InlineKeyboardButton(text="🗑️ Пересоздать БД", callback_data="admin_recreate_db")
        ],
        [
            InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users"),
            InlineKeyboardButton(text="📝 Шаги воронки", callback_data="admin_steps")
        ],
        [
            InlineKeyboardButton(text="🚀 Запустить воронку", callback_data="admin_start_funnel"),
            InlineKeyboardButton(text="⏹️ Остановить воронку", callback_data="admin_stop_funnel")
        ]
    ])
    
    await callback.message.edit_text(
        "🔧 **Панель администратора**\n\n"
        "Выберите действие:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

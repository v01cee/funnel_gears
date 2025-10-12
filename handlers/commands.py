"""Роутер для команд бота"""

from aiogram import Router, types
from aiogram.filters import Command
from .start import cmd_start

# Создаем роутер для команд
commands_router = Router()

# Регистрируем команды
commands_router.message.register(cmd_start, Command("start"))

@commands_router.message(Command("myid"))
async def get_my_id(message: types.Message):
    """Показать ID пользователя"""
    user = message.from_user
    
    text = f"""
🆔 **Ваш ID:** `{user.id}`

📋 **Информация о вас:**
• Имя: {user.first_name or 'Не указано'}
• Фамилия: {user.last_name or 'Не указано'}
• Username: @{user.username or 'Не указано'}
• ID: {user.id}

💡 **Для настройки админки:**
Добавьте этот ID в файл `.env`:
```
ADMIN_ID={user.id}
```

Или в файл `config/settings.py` в переменную `ADMIN_ID`.
"""
    
    await message.answer(text, parse_mode="Markdown")

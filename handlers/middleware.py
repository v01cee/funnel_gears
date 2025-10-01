"""Middleware для бота"""

import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    """Middleware для логирования запросов"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Логируем входящее событие
        if hasattr(event, 'from_user') and event.from_user:
            user_id = event.from_user.id
            username = event.from_user.username or "без username"
            logger.info(f"Получено событие от пользователя {user_id} (@{username})")
        
        # Выполняем обработчик
        result = await handler(event, data)
        
        # Логируем результат
        logger.info("Событие обработано успешно")
        
        return result

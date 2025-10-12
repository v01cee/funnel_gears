"""Настройки таймингов воронки"""

from datetime import timedelta

# Режимы работы воронки
TEST_MODE = True  # True для тестирования (5 секунд), False для продакшна (1 день)

if TEST_MODE:
    # Тестовый режим - все шаги через 5 секунд
    FUNNEL_DELAYS = {
        'hour_letter': timedelta(seconds=5),
        'day_letter': timedelta(seconds=5),
        'quality_letter': timedelta(seconds=5),
        'two_days_letter': timedelta(seconds=5),
        'product2_letter': timedelta(seconds=5),
        'product2_letter2': timedelta(seconds=5),
        'client_story': timedelta(seconds=5),
        'discount_offer': timedelta(seconds=5),
        'ready_kit': timedelta(seconds=5),
        'oto_discount': timedelta(seconds=5),
        'survey': timedelta(seconds=5),
    }
    CHECK_INTERVAL = 2  # Проверка каждые 2 секунды
    MESSAGE_DELAY = 2   # Задержка между сообщениями 2 секунды
else:
    # Продакшн режим - реальные интервалы
    FUNNEL_DELAYS = {
        'hour_letter': timedelta(days=1),
        'day_letter': timedelta(days=1),
        'quality_letter': timedelta(days=1),
        'two_days_letter': timedelta(days=1),
        'product2_letter': timedelta(days=1),
        'product2_letter2': timedelta(days=1),
        'client_story': timedelta(days=1),
        'discount_offer': timedelta(days=1),
        'ready_kit': timedelta(days=1),
        'oto_discount': timedelta(days=1),
        'survey': timedelta(days=1),
    }
    CHECK_INTERVAL = 60  # Проверка каждые 60 секунд
    MESSAGE_DELAY = 5     # Задержка между сообщениями 5 секунд

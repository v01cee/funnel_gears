"""Настройки таймингов воронки"""

from datetime import timedelta

# Режимы работы воронки
TEST_MODE = False  # True для тестирования (5 секунд), False для продакшна (1 день)

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
    # Продакшн режим - оригинальные интервалы воронки
    FUNNEL_DELAYS = {
        'hour_letter': timedelta(hours=1),        # Через 1 час
        'day_letter': timedelta(days=2),          # Через 2 дня (День 2)
        'quality_letter': timedelta(days=2),      # Через 2 дня (День 4)
        'two_days_letter': timedelta(days=3),    # Через 3 дня (День 7)
        'product2_letter': timedelta(days=3),    # Через 3 дня (День 10)
        'product2_letter2': timedelta(days=3),   # Через 3 дня (День 13)
        'client_story': timedelta(days=3),        # Через 3 дня (День 16)
        'discount_offer': timedelta(days=4),      # Через 4 дня (День 20)
        'ready_kit': timedelta(days=7),           # Через 7 дней (День 27)
        'oto_discount': timedelta(days=3),        # Через 3 дня (День 30)
        'survey': timedelta(days=0),               # Последний шаг
    }
    CHECK_INTERVAL = 60  # Проверка каждые 60 секунд
    MESSAGE_DELAY = 0     # Без задержки между сообщениями (как было изначально)

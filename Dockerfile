# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем папку для базы данных
RUN mkdir -p /app/data

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV DATABASE_PATH=/app/data/bot.db

# Открываем порт (если понадобится для веб-интерфейса)
EXPOSE 8000

# Команда запуска
CMD ["python", "bot_main.py"]





# Настройка Git для проекта

## 1. Инициализация Git репозитория

```bash
# Инициализируем Git
git init

# Добавляем все файлы
git add .

# Первый коммит
git commit -m "Initial commit: Telegram bot funnel ready for production"
```

## 2. Создание репозитория на GitHub

1. Зайдите на https://github.com
2. Нажмите "New repository"
3. Название: `telegram-funnel-bot` (или любое другое)
4. Описание: `Telegram bot for sales funnel with automated messaging`
5. Выберите "Public" или "Private"
6. НЕ добавляйте README, .gitignore, license (они уже есть)
7. Нажмите "Create repository"

## 3. Подключение к GitHub

```bash
# Добавляем remote origin (замените YOUR_USERNAME и YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Устанавливаем главную ветку
git branch -M main

# Отправляем код на GitHub
git push -u origin main
```

## 4. Для обновления кода в будущем

```bash
# Добавляем изменения
git add .

# Коммитим
git commit -m "Описание изменений"

# Отправляем на GitHub
git push
```

## 5. Клонирование на сервер

```bash
# Клонируем репозиторий
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Переходим в папку
cd YOUR_REPO

# Создаем .env файл
nano .env

# Запускаем
docker-compose up -d
```

## Важные файлы в репозитории:

- ✅ `bot_main.py` - основной файл
- ✅ `requirements.txt` - зависимости
- ✅ `Dockerfile` - образ Docker
- ✅ `docker-compose.yml` - конфигурация
- ✅ `README.md` - документация
- ✅ `.gitignore` - исключения для Git
- ❌ `.env` - НЕ включается (секретные данные)
- ❌ `data/` - НЕ включается (база данных)
- ❌ `*.db` - НЕ включается (файлы БД)

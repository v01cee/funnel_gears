from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, UserStep
from config.settings import DATABASE_PATH

# Инициализация базы данных
engine = create_engine(f'sqlite:///{DATABASE_PATH}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Создание таблиц в базе данных"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Получение сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserStep(Base):
    """Модель шагов воронки"""
    __tablename__ = "user_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    step_name = Column(String)  # 'hour_letter', 'day_letter', etc.
    scheduled_time = Column(DateTime)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Уникальное ограничение: один пользователь не может иметь два одинаковых шага
    __table_args__ = (
        UniqueConstraint('user_id', 'step_name', name='unique_user_step'),
    )

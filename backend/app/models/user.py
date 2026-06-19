from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Подтверждение почты по коду
    is_verified = Column(Boolean, default=False, nullable=False, server_default="0")
    verification_code = Column(String, nullable=True)
    verification_code_expires_at = Column(DateTime, nullable=True)
    # Подтверждение через Telegram
    telegram_chat_id = Column(String, nullable=True)
    link_token = Column(String, nullable=True, index=True)

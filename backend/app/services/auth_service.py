import secrets
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..core.security import hash_password, verify_password, create_access_token
from ..config import settings
from ..models.user import User
from .email_service import send_verification_email
from .telegram_service import send_telegram_code


def _generate_code() -> str:
    """Сгенерировать 6-значный код подтверждения."""
    return f"{secrets.randbelow(1_000_000):06d}"


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, email: str, password: str) -> User:
        existing = self.repo.get_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        hashed = hash_password(password)
        user = self.repo.create(email=email, hashed_password=hashed)
        # Токен для deep-link Telegram-бота
        user.link_token = secrets.token_urlsafe(16)
        # Создаём и отправляем код подтверждения на почту
        self._issue_code(user)
        return user

    def link_telegram(self, token: str, chat_id: str) -> dict:
        """
        Вызывается ботом при /start <token>. Привязывает Telegram-чат к аккаунту
        и возвращает свежий код подтверждения (бот отправляет его в чат).
        """
        user = self.repo.get_by_link_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid link token",
            )
        if user.is_verified:
            return {"email": user.email, "code": None, "already_verified": True}

        user.telegram_chat_id = str(chat_id)
        code = self._set_code(user)
        self.repo.save(user)
        return {"email": user.email, "code": code, "already_verified": False}

    def verify_code(self, email: str, code: str) -> str:
        user = self.repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )
        if user.is_verified:
            # Уже подтверждён — просто выдаём токен
            return create_access_token(data={"sub": user.email})

        if (
            not user.verification_code
            or not user.verification_code_expires_at
            or user.verification_code_expires_at < datetime.utcnow()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code expired",
            )
        if not secrets.compare_digest(user.verification_code, code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification code",
            )

        user.is_verified = True
        user.verification_code = None
        user.verification_code_expires_at = None
        self.repo.save(user)
        return create_access_token(data={"sub": user.email})

    def resend_code(self, email: str) -> None:
        user = self.repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified",
            )
        self._issue_code(user)

    def authenticate(self, email: str, password: str) -> str:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password OR there is no registered user with that email",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_verified:
            # Каждая попытка входа неподтверждённого аккаунта заново выдаёт код
            # и шлёт его в Telegram (если чат привязан) либо на почту/в консоль.
            self._issue_code(user)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified",
            )
        return create_access_token(data={"sub": user.email})

    def _set_code(self, user: User) -> str:
        """Сгенерировать и записать (в объект) новый код подтверждения. Без сохранения в БД."""
        code = _generate_code()
        user.verification_code = code
        user.verification_code_expires_at = datetime.utcnow() + timedelta(
            minutes=settings.verification_code_ttl_minutes
        )
        return code

    def _issue_code(self, user: User) -> None:
        """Сгенерировать новый код, сохранить и доставить пользователю."""
        code = self._set_code(user)
        self.repo.save(user)
        self._deliver_code(user, code)

    def _deliver_code(self, user: User, code: str) -> None:
        """
        Доставить код пользователю по приоритетному каналу:
        сначала Telegram (если чат привязан и push настроен), иначе — почта/консоль.
        """
        if user.telegram_chat_id and send_telegram_code(user.telegram_chat_id, code):
            return
        send_verification_email(user.email, code)

import secrets
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..core.security import hash_password, verify_password, create_access_token
from ..config import settings
from ..models.user import User
from .email_service import send_verification_email


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
        # Создаём и отправляем код подтверждения
        self._issue_code(user)
        return user

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
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified",
            )
        return create_access_token(data={"sub": user.email})

    def _issue_code(self, user: User) -> None:
        """Сгенерировать новый код, сохранить и отправить письмо."""
        code = _generate_code()
        user.verification_code = code
        user.verification_code_expires_at = datetime.utcnow() + timedelta(
            minutes=settings.verification_code_ttl_minutes
        )
        self.repo.save(user)
        send_verification_email(user.email, code)

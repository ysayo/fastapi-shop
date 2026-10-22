from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..config import settings
from ..services.auth_service import AuthService
from ..schemas.user import (
    UserCreate,
    UserResponse,
    RegisterResponse,
    Token,
    VerifyRequest,
    ResendRequest,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

def _telegram_link(user) -> str | None:
    """Готовая ссылка на бота (None, если бот не настроен)."""
    if settings.telegram_bot_username and user.link_token:
        return f"https://t.me/{settings.telegram_bot_username}?start={user.link_token}"
    return None

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.register(email=user_data.email, password=user_data.password)
    return RegisterResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        telegram_link=_telegram_link(user),
    )

@router.post("/verify", response_model=Token)
def verify(data: VerifyRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    token = service.verify_code(email=data.email, code=data.code)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/resend-code", status_code=status.HTTP_202_ACCEPTED)
def resend_code(data: ResendRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    service.resend_code(email=data.email)
    return {"message": "Verification code sent"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.authenticate(email=form_data.username, password=form_data.password)
    # Двухфакторность: токен выдаётся только после ввода кода на /verify.
    # Вместе с 403 отдаём ссылку на бота, чтобы код можно было получить в Telegram.
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": "Verification code required",
            "telegram_link": _telegram_link(user),
        },
    )

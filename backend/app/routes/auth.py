from fastapi import APIRouter, Depends, status
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

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.register(email=user_data.email, password=user_data.password)
    # Готовая ссылка на бота (если он настроен)
    telegram_link = None
    if settings.telegram_bot_username and user.link_token:
        telegram_link = f"https://t.me/{settings.telegram_bot_username}?start={user.link_token}"
    return RegisterResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        telegram_link=telegram_link,
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
    token = service.authenticate(email=form_data.username, password=form_data.password)
    return {"access_token": token, "token_type": "bearer"}

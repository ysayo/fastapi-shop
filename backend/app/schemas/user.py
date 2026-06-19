from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    is_verified: bool

    model_config = {"from_attributes": True}

class RegisterResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    is_verified: bool
    # Готовая ссылка на Telegram-бота для подтверждения (None, если бот не настроен)
    telegram_link: str | None = None

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class VerifyRequest(BaseModel):
    email: EmailStr
    code: str

class ResendRequest(BaseModel):
    email: EmailStr

class TelegramLinkRequest(BaseModel):
    token: str
    chat_id: str
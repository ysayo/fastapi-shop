from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    app_name: str = "FastAPI Shop"
    debug: bool = True
    database_url: str = "sqlite:///./shop.db"
    cors_origins: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    static_dir: str = "static"
    images_dir: str = "static/images"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    # access_token: str = ""
    access_token_expire_minutes: int = 30
    # refresh_token: str = ""

    # Подтверждение почты по коду (Brevo)
    # Если brevo_api_key пуст — код выводится в консоль вместо отправки письма.
    brevo_api_key: str = ""
    email_from: str = ""              # подтверждённый адрес-отправитель в Brevo
    email_from_name: str = "FastAPI Shop"
    verification_code_ttl_minutes: int = 15

    class Config:
        env_file = ".env"

settings = Settings()

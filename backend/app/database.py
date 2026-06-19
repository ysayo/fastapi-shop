from sqlalchemy import create_engine, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    _migrate_user_columns()


def _migrate_user_columns():
    """
    Лёгкая авто-миграция: добавляет недостающие колонки подтверждения почты
    в существующую таблицу users (create_all не изменяет уже созданные таблицы).
    """
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    existing = {col["name"] for col in inspector.get_columns("users")}
    new_columns = {
        "is_verified": "BOOLEAN NOT NULL DEFAULT 0",
        "verification_code": "VARCHAR",
        "verification_code_expires_at": "DATETIME",
        "telegram_chat_id": "VARCHAR",
        "link_token": "VARCHAR",
    }
    with engine.begin() as conn:
        for name, ddl in new_columns.items():
            if name not in existing:
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {name} {ddl}"))
        # Существующие до миграции аккаунты считаем подтверждёнными,
        # чтобы не заблокировать им вход.
        if "is_verified" not in existing:
            conn.execute(text("UPDATE users SET is_verified = 1"))

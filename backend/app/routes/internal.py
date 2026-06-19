import secrets
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..config import settings
from ..services.auth_service import AuthService
from ..schemas.user import TelegramLinkRequest

# Внутренний роутер для межсервисного общения (Telegram-бот -> backend).
# Защищён общим секретом, наружу выставлять не нужно.
router = APIRouter(prefix="/api/internal", tags=["internal"])


@router.post("/telegram/link")
def telegram_link(
    data: TelegramLinkRequest,
    x_internal_secret: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not settings.telegram_internal_secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Telegram integration is not configured",
        )
    if not x_internal_secret or not secrets.compare_digest(
        x_internal_secret, settings.telegram_internal_secret
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    service = AuthService(db)
    return service.link_telegram(token=data.token, chat_id=data.chat_id)

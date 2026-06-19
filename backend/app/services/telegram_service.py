"""
Сервис отправки сообщений через Telegram Bot API.

В отличие от сервиса telegram-bot (который реагирует на команды пользователя),
здесь backend САМ инициирует отправку — пушит код подтверждения в уже привязанный
чат. Используется тот же токен бота (TELEGRAM_BOT_TOKEN).

Если токен не задан — отправка отключена, и код уходит другим каналом
(почта/консоль). Сетевые ошибки не роняют запрос, а логируются.
"""

import logging
import httpx
from ..config import settings

logger = logging.getLogger("telegram")

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def is_telegram_enabled() -> bool:
    """Настроен ли push-канал Telegram (есть токен бота)."""
    return bool(settings.telegram_bot_token)


def log_telegram_mode() -> None:
    """Сообщить в лог, доступна ли отправка кодов через Telegram."""
    if is_telegram_enabled():
        logger.info("Telegram: push-отправка кодов включена.")
    else:
        logger.warning(
            "Telegram: push-отправка ОТКЛЮЧЕНА (нет TELEGRAM_BOT_TOKEN). "
            "Коды для привязанных чатов отправляться не будут."
        )


def send_telegram_code(chat_id: str, code: str) -> bool:
    """
    Отправить код подтверждения в Telegram-чат.

    Возвращает True при успешной отправке, иначе False — чтобы вызывающий код
    мог откатиться на запасной канал (почту/консоль).
    """
    if not is_telegram_enabled():
        return False

    text = (
        "Ваш код подтверждения для <b>FastAPI Shop</b>:\n\n"
        f"<code>{code}</code>\n\n"
        f"Код действует {settings.verification_code_ttl_minutes} минут.\n"
        "Если вы ничего не запрашивали — просто проигнорируйте это сообщение."
    )

    try:
        response = httpx.post(
            TELEGRAM_API_URL.format(token=settings.telegram_bot_token),
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=10.0,
        )
    except httpx.HTTPError as exc:
        logger.error("Telegram unreachable: %s", exc)
        return False

    if response.status_code >= 400:
        logger.error("Telegram error %s: %s", response.status_code, response.text)
        return False

    return True

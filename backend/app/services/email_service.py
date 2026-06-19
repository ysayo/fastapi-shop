"""
Сервис отправки писем через Brevo (https://www.brevo.com).

Если в настройках не задан brevo_api_key или email_from — письмо не отправляется,
а код подтверждения выводится в консоль (удобно для локальной разработки).
"""

import logging
import httpx
from ..config import settings

logger = logging.getLogger("email")

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def is_real_sending_enabled() -> bool:
    """Настроена ли реальная отправка писем (есть ключ и отправитель)."""
    return bool(settings.brevo_api_key and settings.email_from)


def log_email_mode() -> None:
    """Сообщить в лог, в каком режиме работает отправка писем."""
    if is_real_sending_enabled():
        logger.info("Email: реальная отправка через Brevo (отправитель %s)", settings.email_from)
    else:
        logger.warning(
            "Email: РЕЖИМ КОНСОЛИ — письма НЕ отправляются, код печатается в терминал. "
            "Заполните BREVO_API_KEY и EMAIL_FROM в backend/.env для реальной отправки."
        )


def send_verification_email(to_email: str, code: str) -> None:
    """Отправить письмо с кодом подтверждения почты."""
    subject = "Код подтверждения — FastAPI Shop"
    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
            <h2>Подтверждение почты</h2>
            <p>Ваш код подтверждения для FastAPI Shop:</p>
            <p style="font-size: 32px; font-weight: bold; letter-spacing: 6px;">{code}</p>
            <p style="color: #666;">Код действует {settings.verification_code_ttl_minutes} минут.
            Если вы не регистрировались — просто проигнорируйте это письмо.</p>
        </div>
    """

    # Нет ключа/отправителя — режим разработки: печатаем код в консоль
    if not is_real_sending_enabled():
        logger.warning(
            "[DEV] Email не настроен (нет BREVO_API_KEY/EMAIL_FROM). "
            "Код подтверждения для %s: %s",
            to_email,
            code,
        )
        print(f"\n[DEV] Код подтверждения для {to_email}: {code}\n")
        return

    payload = {
        "sender": {"name": settings.email_from_name, "email": settings.email_from},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html,
    }
    headers = {
        "api-key": settings.brevo_api_key,
        "content-type": "application/json",
        "accept": "application/json",
    }

    response = httpx.post(BREVO_API_URL, json=payload, headers=headers, timeout=10.0)
    if response.status_code >= 400:
        logger.error("Brevo error %s: %s", response.status_code, response.text)
        raise RuntimeError("Не удалось отправить письмо с кодом подтверждения")

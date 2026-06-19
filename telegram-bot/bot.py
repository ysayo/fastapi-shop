"""
Telegram-бот подтверждения почты для FastAPI Shop (aiogram 3.x).

Архитектура: бот — отдельный сервис. Он НЕ ходит в БД напрямую,
а вызывает внутренний эндпоинт backend'а (защищён общим секретом).

Поток:
  1. Пользователь регистрируется на сайте → backend выдаёт deep-link
     вида https://t.me/<bot>?start=<token>.
  2. Пользователь жмёт «Старт» → сюда приходит /start <token>.
  3. Бот зовёт backend /api/internal/telegram/link → получает код.
  4. Бот отправляет код в чат, пользователь вводит его на сайте.
"""

import asyncio
import logging
import os

import httpx
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message

# Локальный запуск: подхватываем telegram-bot/.env, если он есть.
# В Docker переменные приходят из docker-compose, файла нет — это ок.
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")


def _require(name: str) -> str:
    """Прочитать обязательную переменную окружения или завершиться с понятной ошибкой."""
    value = os.environ.get(name)
    if not value:
        raise SystemExit(
            f"Переменная {name} не задана.\n"
            f"Укажите её в переменных окружения или в файле telegram-bot/.env.\n"
            f"Пример .env:\n"
            f"  BOT_TOKEN=123456:ABC...        # токен от @BotFather\n"
            f"  INTERNAL_SECRET=<секрет>        # = TELEGRAM_INTERNAL_SECRET бэкенда\n"
            f"  BACKEND_URL=http://localhost:8000"
        )
    return value


# По умолчанию backend на localhost (локальный запуск); в Docker URL задаёт compose.
BOT_TOKEN = _require("BOT_TOKEN")
INTERNAL_SECRET = _require("INTERNAL_SECRET")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000").rstrip("/")

dp = Dispatcher()


@dp.message(CommandStart(deep_link=True))
async def on_start_with_token(message: Message, command: CommandObject) -> None:
    """Обработка /start <token> — привязка чата и отправка кода."""
    token = (command.args or "").strip()
    if not token:
        await on_start_plain(message)
        return

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{BACKEND_URL}/api/internal/telegram/link",
                json={"token": token, "chat_id": str(message.chat.id)},
                headers={"X-Internal-Secret": INTERNAL_SECRET},
            )
    except httpx.HTTPError as exc:
        logger.error("Backend unreachable: %s", exc)
        await message.answer("Сервис временно недоступен. Попробуйте позже.")
        return

    if resp.status_code == 200:
        data = resp.json()
        if data.get("already_verified"):
            await message.answer("Эта почта уже подтверждена. Можете войти на сайте.")
            return
        code = data.get("code")
        await message.answer(
            "Ваш код подтверждения для <b>FastAPI Shop</b>:\n\n"
            f"<code>{code}</code>\n\n"
            "Введите его на сайте, чтобы завершить регистрацию.",
            parse_mode="HTML",
        )
    elif resp.status_code == 400:
        await message.answer(
            "Ссылка недействительна или устарела. Зарегистрируйтесь заново на сайте."
        )
    else:
        logger.error("Unexpected backend response %s: %s", resp.status_code, resp.text)
        await message.answer("Не удалось получить код. Попробуйте позже.")


@dp.message(CommandStart())
async def on_start_plain(message: Message) -> None:
    """/start без токена — подсказываем, как пользоваться."""
    await message.answer(
        "Привет! Это бот подтверждения почты FastAPI Shop.\n"
        "Чтобы получить код, начните регистрацию на сайте и нажмите там кнопку "
        "«Подтвердить через Telegram»."
    )


async def main() -> None:
    bot = Bot(BOT_TOKEN)
    logger.info("Bot started, polling... (backend: %s)", BACKEND_URL)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

# backend/translate_content.py
"""
Автоперевод контента из БД (названия/описания товаров и названия категорий)
на русский и английский.

Использует deep-translator (GoogleTranslator) — БЕЗ API-ключа.

Логика:
  • источник перевода — базовое поле (name / description), язык определяется авто;
  • заполняются пустые *_ru / *_en (идемпотентно — повторный запуск ничего не ломает);
  • с флагом --force перезаписывает уже существующие переводы.

Запуск:
    python translate_content.py            # заполнить только пустые переводы
    python translate_content.py --force    # перевести заново всё
"""

import sys
import time

from deep_translator import GoogleTranslator

from app.database import SessionLocal, init_db
from app.models.category import Category
from app.models.product import Product

FORCE = "--force" in sys.argv
TARGET_LANGS = ("ru", "en")


def translate(text: str, target: str) -> str:
    """Перевести текст на target-язык. При ошибке вернуть исходный текст."""
    text = (text or "").strip()
    if not text:
        return ""
    try:
        return GoogleTranslator(source="auto", target=target).translate(text)
    except Exception as exc:  # сеть/лимиты — не валим весь прогон
        print(f"   ⚠️  Не удалось перевести на {target}: {exc}")
        return text


def fill_field(obj, base_field: str) -> bool:
    """
    Заполнить <base_field>_ru и <base_field>_en для объекта.
    Возвращает True, если что-то изменилось.
    """
    source = getattr(obj, base_field, None)
    if not source:
        return False

    changed = False
    for lang in TARGET_LANGS:
        attr = f"{base_field}_{lang}"
        if FORCE or not getattr(obj, attr, None):
            setattr(obj, attr, translate(source, lang))
            changed = True
            time.sleep(0.2)  # бережём бесплатный endpoint
    return changed


def main() -> None:
    print("🌍 Автоперевод контента...")
    init_db()  # на случай, если колонки локализации ещё не добавлены
    db = SessionLocal()
    try:
        categories = db.query(Category).all()
        for cat in categories:
            if fill_field(cat, "name"):
                print(f"   • категория «{cat.name}» → ru/en")

        products = db.query(Product).all()
        for prod in products:
            touched = []
            if fill_field(prod, "name"):
                touched.append("name")
            if fill_field(prod, "description"):
                touched.append("description")
            if touched:
                print(f"   • товар «{prod.name}» → {', '.join(touched)}")

        db.commit()
        print(f"✅ Готово: {len(categories)} категорий, {len(products)} товаров.")
    except Exception as exc:
        db.rollback()
        print(f"❌ Ошибка: {exc}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

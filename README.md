
# 🛍️ FastAPI Shop - Полнофункциональный интернет-магазин

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python) ![FastAPI](https://img.shields.io/badge/FastAPI-0.119.0-009688?style=for-the-badge&logo=fastapi) ![Vue.js](https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=for-the-badge&logo=vue.js) ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)

Современный, масштабируемый интернет-магазин с REST API на FastAPI и SPA frontend на Vue.js 3

</div>

---

## 🎯 О проекте

**FastAPI Shop** - это современное веб-приложение для электронной коммерции. Проект демонстрирует best practices разработки full-stack приложений с разделением backend и frontend.

### ✨ Ключевые возможности

- 🛒 **Управление корзиной** - добавление, удаление, изменение количества товаров
- 📦 **Каталог товаров** - просмотр товаров с фильтрацией по категориям
- 🔍 **Детальная информация** - подробные страницы товаров
- 🔐 **Аутентификация** - регистрация и вход с JWT-токенами
- ✅ **Подтверждение кодом** - код приходит в **Telegram** (или на почту/в консоль), 2FA при каждом входе
- 🤖 **Telegram-бот** - отдельный сервис для привязки аккаунта и доставки кодов
- 🌍 **Локализация (RU/EN)** - интерфейс и контент из БД, с автопереводом
- 🌗 **Тёмная / светлая тема** - переключатель с сохранением выбора
- 💾 **Персистентность данных** - сохранение корзины в localStorage
- 🎨 **Современный UI** - адаптивный дизайн на Tailwind CSS
- 🚀 **Production-ready** - Docker, Nginx, SSL, CI/CD на GitLab

---

## 📁 Структура проекта

```
fastapi-shop/
│
├── backend/                      # Backend часть (FastAPI)
│   ├── app/
│   │   ├── models/              # SQLAlchemy модели БД
│   │   │   ├── category.py     # Категории (+ name_ru/name_en)
│   │   │   ├── product.py      # Товары (+ локализация, авто created_at)
│   │   │   └── user.py         # Пользователи (код подтверждения, telegram_chat_id)
│   │   │
│   │   ├── schemas/             # Pydantic схемы для валидации
│   │   │   ├── cart.py         # Схемы корзины
│   │   │   ├── category.py     # Схемы категорий
│   │   │   ├── product.py      # Схемы товаров
│   │   │   └── user.py         # Схемы регистрации/входа/подтверждения
│   │   │
│   │   ├── repositories/        # Слой работы с БД (Repository Pattern)
│   │   │   ├── category_repository.py
│   │   │   ├── product_repository.py
│   │   │   └── user_repository.py
│   │   │
│   │   ├── services/            # Бизнес-логика приложения
│   │   │   ├── cart_service.py
│   │   │   ├── category_service.py
│   │   │   ├── product_service.py
│   │   │   ├── auth_service.py      # Регистрация, вход, коды, 2FA
│   │   │   ├── email_service.py     # Отправка кода на почту (Brevo)
│   │   │   └── telegram_service.py  # Push кода в Telegram (Bot API)
│   │   │
│   │   ├── routes/              # API endpoints (Controllers)
│   │   │   ├── cart.py         # Эндпоинты корзины
│   │   │   ├── categories.py   # Эндпоинты категорий
│   │   │   ├── products.py     # Эндпоинты товаров
│   │   │   ├── auth.py         # Регистрация / вход / подтверждение
│   │   │   └── internal.py     # Внутренний эндпоинт для Telegram-бота
│   │   │
│   │   ├── core/                # Безопасность (хеш паролей, JWT)
│   │   │   └── security.py
│   │   ├── dependencies/        # FastAPI-зависимости (текущий пользователь)
│   │   │   └── auth.py
│   │   ├── config.py            # Конфигурация приложения (pydantic-settings)
│   │   ├── database.py          # SQLAlchemy + лёгкие авто-миграции
│   │   └── main.py              # Точка входа FastAPI
│   │
│   ├── static/images/           # Статические файлы (изображения)
│   ├── Dockerfile               # Docker образ backend
│   ├── requirements.txt         # Python зависимости
│   ├── run.py                   # Скрипт запуска сервера
│   ├── seed_data.py             # Заполнение БД тестовыми данными
│   └── translate_content.py     # Автоперевод контента (deep-translator)
│
├── frontend/                     # Frontend часть (Vue.js 3)
│   ├── src/
│   │   ├── components/          # Vue компоненты
│   │   │   ├── CartItem.vue           # Элемент корзины
│   │   │   ├── CategoryFilter.vue     # Фильтр категорий
│   │   │   ├── Header.vue             # Шапка (навигация, тема, язык)
│   │   │   ├── ProductCard.vue        # Карточка товара
│   │   │   ├── AuthForm.vue           # Форма входа/регистрации
│   │   │   ├── PasswordInput.vue      # Поле пароля с показом
│   │   │   └── LanguageSwitcher.vue   # Переключатель RU/EN
│   │   │
│   │   ├── views/               # Страницы приложения
│   │   │   ├── HomePage.vue           # Главная (каталог)
│   │   │   ├── ProductDetailPage.vue  # Детали товара
│   │   │   ├── CartPage.vue           # Корзина
│   │   │   ├── LoginPage.vue          # Вход
│   │   │   ├── RegisterPage.vue       # Регистрация
│   │   │   └── VerifyPage.vue         # Ввод кода подтверждения
│   │   │
│   │   ├── stores/              # Pinia stores (State Management)
│   │   │   ├── cart.js         # Store корзины
│   │   │   ├── products.js     # Store товаров
│   │   │   └── auth.js         # Store аутентификации (JWT, email)
│   │   │
│   │   ├── composables/         # Переиспользуемая логика
│   │   │   ├── useCategoryName.js     # Локализованное имя категории
│   │   │   ├── useLocalized.js        # Выбор поля по языку (name_ru/en…)
│   │   │   ├── useTheme.js            # Тёмная/светлая тема
│   │   │   └── useAuthErrorMessage.js # Тексты ошибок авторизации
│   │   │
│   │   ├── i18n/                # Интернационализация (vue-i18n)
│   │   │   ├── index.js        # Настройка локалей и плюрализации
│   │   │   └── locales/        # ru.js / en.js — строки интерфейса
│   │   │
│   │   ├── services/            # API клиенты
│   │   │   └── api.js          # Axios конфигурация и методы
│   │   │
│   │   ├── router/              # Vue Router конфигурация
│   │   │   └── index.js        # Определение маршрутов
│   │   │
│   │   ├── assets/              # Статические ресурсы
│   │   ├── App.vue              # Корневой компонент
│   │   └── main.js              # Точка входа приложения
│   │
│   ├── index.html               # HTML + конфиг Tailwind (тема, палитра)
│   ├── Dockerfile               # Docker образ frontend
│   ├── nginx.conf               # Конфигурация Nginx для SPA
│   ├── package.json             # NPM зависимости
│   └── vite.config.js          # Конфигурация Vite
│
├── telegram-bot/                 # Telegram-бот подтверждения (aiogram)
│   ├── bot.py                   # Логика бота (/start, привязка чата)
│   ├── Dockerfile               # Docker образ бота
│   └── requirements.txt         # Зависимости бота
│
├── nginx/                        # Reverse proxy конфигурация
│   └── nginx.conf               # Главная конфигурация Nginx
│
├── .gitlab-ci.yml                # CI/CD пайплайн (lint / build / deploy)
├── docker-compose.yml            # Оркестрация Docker контейнеров
└── README.md                     # Документация проекта
```

### 🔍 Назначение компонентов

#### Backend (FastAPI)

|Компонент|Назначение|
|---|---|
|**models/**|SQLAlchemy модели для работы с БД (ORM)|
|**schemas/**|Pydantic схемы для валидации входящих/исходящих данных|
|**repositories/**|Инкапсуляция логики работы с БД (Repository Pattern)|
|**services/**|Бизнес-логика: товары, корзина, аутентификация, почта, Telegram|
|**routes/**|HTTP endpoints и маршрутизация (Controllers)|
|**core/**|Безопасность: хеширование паролей, создание/проверка JWT|
|**dependencies/**|FastAPI-зависимости (получение текущего пользователя по токену)|
|**config.py**|Настройки приложения (CORS, DB, почта, Telegram)|
|**database.py**|SQLAlchemy, сессии и лёгкие авто-миграции колонок|
|**main.py**|Инициализация FastAPI, подключение middleware и роутеров|

#### Frontend (Vue.js 3)

|Компонент|Назначение|
|---|---|
|**components/**|Переиспользуемые UI компоненты|
|**views/**|Страницы приложения (роутинг)|
|**stores/**|Глобальное состояние: корзина, товары, аутентификация (Pinia)|
|**composables/**|Переиспользуемая логика: локализация, тема, ошибки авторизации|
|**i18n/**|Интернационализация: настройка и строки RU/EN (vue-i18n)|
|**services/**|HTTP клиент для взаимодействия с API|
|**router/**|Конфигурация маршрутизации (Vue Router)|

---

## 🛠 Технологический стек

### Backend

- **FastAPI** 0.119.0 - современный, быстрый web-framework
- **SQLAlchemy** 2.0.44 - ORM для работы с базой данных
- **Pydantic** 2.12.1 - валидация данных и настроек
- **SQLite** - легковесная реляционная СУБД
- **Uvicorn** - ASGI сервер для production
- **python-jose** + **passlib/bcrypt** - JWT-токены и хеширование паролей
- **Brevo API** - отправка писем с кодом подтверждения (опционально)
- **deep-translator** - автоперевод контента (без API-ключа)

### Telegram-бот

- **aiogram** 3.13 - асинхронный фреймворк для Telegram Bot API
- **httpx** - HTTP-клиент для вызова внутреннего эндпоинта backend

### Frontend

- **Vue.js** 3.5.22 - прогрессивный JavaScript фреймворк
- **Pinia** 3.0.3 - официальный state management для Vue 3
- **Vue Router** 4.5.1 - роутинг для SPA
- **vue-i18n** 11 - интернационализация (RU/EN)
- **Axios** 1.12.2 - HTTP клиент
- **Tailwind CSS** - utility-first CSS фреймворк (тёмная тема, кастомная палитра)
- **Vite** 7.1.7 - быстрый build tool

### DevOps

- **Docker** - контейнеризация приложений
- **Docker Compose** - оркестрация multi-container приложений
- **Nginx** - reverse proxy и веб-сервер
- **GitLab CI/CD** - автоматические проверки, сборка и деплой

---

## 🔄 CI/CD

Пайплайн описан в [`.gitlab-ci.yml`](.gitlab-ci.yml) и состоит из трёх стадий:

| Стадия   | Что делает                                                                 |
| -------- | -------------------------------------------------------------------------- |
| `lint`   | ESLint для фронтенда + проверка компиляции бэкенда (`compileall`)          |
| `build`  | Продакшен-сборка фронтенда (Vite), артефакт `frontend/dist`                |
| `deploy` | Ручной деплой по SSH на сервер (только из ветки по умолчанию)              |

Стадии `lint` и `build` запускаются автоматически для каждого merge request'а
и пуша в ветку. Деплой запускается вручную кнопкой в интерфейсе GitLab и
выполняет на сервере `git pull` + `docker compose up -d --build`.

### Переменные для деплоя

Задаются в **Settings → CI/CD → Variables**:

| Переменная        | Назначение                                          | Тип      |
| ----------------- | --------------------------------------------------- | -------- |
| `SSH_PRIVATE_KEY` | Приватный SSH-ключ для доступа к серверу             | File     |
| `SSH_HOST`        | Адрес сервера                                        | Variable |
| `SSH_USER`        | Пользователь на сервере                              | Variable |
| `DEPLOY_PATH`     | Путь до репозитория на сервере                       | Variable |
| `DOMAIN`          | Домен приложения (ссылка на окружение)               | Variable |

---

## 🔐 Аутентификация и подтверждение

Регистрация и вход построены на JWT. Подтверждение аккаунта — кодом из 6 цифр.

**Поток:**

1. **Регистрация** (`POST /api/auth/register`) → создаётся пользователь, генерируется код и `link_token` для Telegram. Код доставляется доступным каналом (Telegram → почта → консоль).
2. **Подтверждение** (`POST /api/auth/verify`) → пользователь вводит код, получает JWT-токен.
3. **Вход** (`POST /api/auth/login`) → при верном пароле **всегда** выдаётся новый код и возвращается `403` (двухфакторность). Фронтенд показывает окно ввода кода → `verify` → токен.
4. **Повторная отправка** (`POST /api/auth/resend-code`) → новый код тем же каналом.

**Доставка кода** (`auth_service._deliver_code`): сначала пробуем **Telegram** (если чат привязан и задан `TELEGRAM_BOT_TOKEN`), иначе — **почту** (Brevo), иначе печатаем код **в консоль backend** (удобно для локальной разработки — никаких ключей не нужно).

---

## 🤖 Telegram-бот

Отдельный сервис (`telegram-bot/`, aiogram) — не ходит в БД напрямую, а общается с backend через защищённый внутренний эндпоинт.

**Как привязывается аккаунт:**

1. После регистрации backend отдаёт deep-link `https://t.me/<bot>?start=<link_token>` (его можно показать кнопкой или QR).
2. Пользователь жмёт **Start** → бот вызывает `POST /api/internal/telegram/link` (с заголовком `X-Internal-Secret`).
3. Backend сохраняет `telegram_chat_id` и возвращает свежий код → бот присылает его в чат.
4. Дальше backend сам шлёт коды в этот чат (push) при логине и повторной отправке.

**Запуск бота локально:**

```bash
cd telegram-bot
pip install -r requirements.txt
# создать .env (см. раздел «Переменные окружения») и запустить:
python bot.py
```

> `INTERNAL_SECRET` бота **должен совпадать** с `TELEGRAM_INTERNAL_SECRET` бэкенда, а `BOT_TOKEN` — с `TELEGRAM_BOT_TOKEN` бэкенда (один и тот же токен от [@BotFather](https://t.me/BotFather)).

---

## 🌍 Локализация (i18n) и автоперевод

Поддерживаются русский и английский. Текст бывает двух видов:

- **Интерфейс** (кнопки, заголовки) — статические строки в `frontend/src/i18n/locales/{ru,en}.js`, доступ через `t('ключ')`.
- **Контент из БД** (названия, описания товаров, категории) — хранится в локализованных колонках `name_ru/name_en`, `description_ru/description_en`. API отдаёт все языки сразу, а композабл [`useLocalized`](frontend/src/composables/useLocalized.js) выбирает нужный по текущему языку. Переключение языка — **мгновенное, без перезапроса** к API. Фолбэк: `<поле>_<язык>` → `_en` → базовое поле.

**Автоперевод** заполняет локализованные поля без API-ключа (через `deep-translator` / Google):

```bash
cd backend
python translate_content.py          # перевести пустые поля
python translate_content.py --force  # перевести заново всё
```

Добавил товар или категорию → прогнал скрипт → переводы готовы. **Код фронта менять не нужно.**

---

## 🌗 Тема оформления

Переключатель светлой/тёмной темы в шапке. Выбор сохраняется в `localStorage` и применяется до рендера (без вспышки). Реализовано на Tailwind `darkMode: 'class'` + композабл [`useTheme`](frontend/src/composables/useTheme.js).

---

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.11+
- Node.js 20+
- npm/yarn
- Git

### Локальная разработка

#### Запуск Backend

```bash
# Переход в директорию backend
cd backend

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt

# Заполнение базы данных тестовыми данными
python seed_data.py

# Запуск сервера разработки
python run.py
```

Backend будет доступен по адресу: **http://localhost:8000**
API документация (Swagger UI): **http://localhost:8000/api/docs**

#### Запуск Frontend

```bash
# Переход в директорию frontend (новый терминал)
cd frontend

# Установка зависимостей
npm install

# Запуск dev сервера
npm run dev
```

Frontend будет доступен по адресу: **http://localhost:5173**

#### Запуск Telegram-бота (опционально)

```bash
cd telegram-bot
pip install -r requirements.txt
# создайте .env (см. ниже) и запустите:
python bot.py
```

> Без бота приложение работает: код подтверждения печатается в консоль backend.

### ⚙️ Переменные окружения

Секреты хранятся в `.env`-файлах (они в `.gitignore` и в репозиторий не попадают).

**`backend/.env`:**

| Переменная | Назначение | Обязательна |
|---|---|---|
| `BREVO_API_KEY` | Ключ Brevo для отправки писем (пусто → код в консоль) | нет |
| `EMAIL_FROM` | Подтверждённый адрес-отправитель в Brevo | нет |
| `TELEGRAM_INTERNAL_SECRET` | Общий секрет с ботом (любая длинная строка) | для Telegram |
| `TELEGRAM_BOT_USERNAME` | Username бота без `@` (для deep-link) | для Telegram |
| `TELEGRAM_BOT_TOKEN` | Токен бота — нужен backend'у для push кодов | для Telegram |
| `VERIFICATION_CODE_TTL_MINUTES` | Время жизни кода (по умолчанию 15) | нет |
| `SECRET_KEY` | Ключ для подписи JWT (смените в production!) | да (prod) |

**`telegram-bot/.env`:**

| Переменная | Назначение |
|---|---|
| `BOT_TOKEN` | Токен от [@BotFather](https://t.me/BotFather) (= `TELEGRAM_BOT_TOKEN`) |
| `INTERNAL_SECRET` | = `TELEGRAM_INTERNAL_SECRET` бэкенда |
| `BACKEND_URL` | Адрес backend (локально `http://localhost:8000`) |

> Сгенерировать секрет: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

### 🐳 Запуск через Docker (весь стек сразу)

```bash
# в корне проекта, заполнив переменные окружения
docker compose up -d --build
```

Поднимет backend, frontend, Telegram-бот, Nginx и Certbot одной командой.

---

## 📚 API документация

### Основные endpoints

#### Products (Товары)

|Метод|Endpoint|Описание|
|---|---|---|
|GET|`/api/products`|Получить все товары|
|GET|`/api/products/{id}`|Получить товар по ID|
|GET|`/api/products/category/{category_id}`|Товары по категории|

#### Categories (Категории)

|Метод|Endpoint|Описание|
|---|---|---|
|GET|`/api/categories`|Получить все категории|
|GET|`/api/categories/{id}`|Получить категорию по ID|

#### Cart (Корзина)

|Метод|Endpoint|Описание|
|---|---|---|
|POST|`/api/cart/add`|Добавить товар в корзину|
|POST|`/api/cart`|Получить содержимое корзины|
|PUT|`/api/cart/update`|Обновить количество товара|
|DELETE|`/api/cart/remove/{id}`|Удалить товар из корзины|

#### Auth (Аутентификация)

|Метод|Endpoint|Описание|
|---|---|---|
|POST|`/api/auth/register`|Регистрация, возвращает `telegram_link` для привязки|
|POST|`/api/auth/verify`|Подтвердить код → выдать JWT-токен|
|POST|`/api/auth/login`|Вход (form-data); при успехе шлёт код и возвращает `403`|
|POST|`/api/auth/resend-code`|Повторно отправить код подтверждения|
|GET|`/api/products/me/test`|Пример защищённого эндпоинта (нужен Bearer-токен)|

#### Internal / System

|Метод|Endpoint|Описание|
|---|---|---|
|POST|`/api/internal/telegram/link`|Привязка чата ботом (защищён `X-Internal-Secret`)|
|GET|`/health`|Проверка работоспособности|
|GET|`/`|Приветствие + ссылка на документацию|

### Примеры запросов

#### Получить все товары

```bash
curl -X GET "http://localhost:8000/api/products"
```

**Ответ:**

```json
{
  "products": [
    {
      "id": 1,
      "name": "Wireless Headphones",
      "description": "High-quality wireless headphones...",
      "name_ru": "Беспроводные наушники",
      "name_en": "Wireless Headphones",
      "description_ru": "Высококачественные беспроводные наушники...",
      "description_en": "High-quality wireless headphones...",
      "price": 299.99,
      "category_id": 1,
      "image_url": "https://...",
      "created_at": "2025-10-16T10:30:00",
      "category": {
        "id": 1,
        "name": "Electronics",
        "slug": "electronics",
        "name_ru": "Электроника",
        "name_en": "Electronics"
      }
    }
  ],
  "total": 13
}
```

#### Добавить товар в корзину

```bash
curl -X POST "http://localhost:8000/api/cart/add" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2,
    "cart": {}
  }'
```

**Ответ:**

```json
{
  "cart": {
    "1": 2
  }
}
```

Полная документация API с интерактивными примерами доступна по адресу:
**http://localhost:8000/api/docs** (Swagger UI)

---


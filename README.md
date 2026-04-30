
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
- 💾 **Персистентность данных** - сохранение корзины в localStorage
- 🎨 **Современный UI** - адаптивный дизайн на Tailwind CSS
- 🚀 **Production-ready** - автоматический деплой с SSL сертификатами

---

## 📁 Структура проекта

```
fastapi-shop/
│
├── backend/                      # Backend часть (FastAPI)
│   ├── app/
│   │   ├── models/              # SQLAlchemy модели БД
│   │   │   ├── category.py     # Модель категорий
│   │   │   └── product.py      # Модель товаров
│   │   │
│   │   ├── schemas/             # Pydantic схемы для валидации
│   │   │   ├── cart.py         # Схемы корзины
│   │   │   ├── category.py     # Схемы категорий
│   │   │   └── product.py      # Схемы товаров
│   │   │
│   │   ├── repositories/        # Слой работы с БД (Repository Pattern)
│   │   │   ├── category_repository.py
│   │   │   └── product_repository.py
│   │   │
│   │   ├── services/            # Бизнес-логика приложения
│   │   │   ├── cart_service.py
│   │   │   ├── category_service.py
│   │   │   └── product_service.py
│   │   │
│   │   ├── routes/              # API endpoints (Controllers)
│   │   │   ├── cart.py         # Эндпоинты корзины
│   │   │   ├── categories.py   # Эндпоинты категорий
│   │   │   └── products.py     # Эндпоинты товаров
│   │   │
│   │   ├── config.py            # Конфигурация приложения
│   │   ├── database.py          # Настройка SQLAlchemy
│   │   └── main.py              # Точка входа FastAPI
│   │
│   ├── static/images/           # Статические файлы (изображения)
│   ├── Dockerfile               # Docker образ backend
│   ├── requirements.txt         # Python зависимости
│   ├── run.py                   # Скрипт запуска сервера
│   └── seed_data.py            # Заполнение БД тестовыми данными
│
├── frontend/                     # Frontend часть (Vue.js 3)
│   ├── src/
│   │   ├── components/          # Vue компоненты
│   │   │   ├── CartItem.vue    # Элемент корзины
│   │   │   ├── CategoryFilter.vue  # Фильтр категорий
│   │   │   ├── Header.vue      # Шапка сайта
│   │   │   └── ProductCard.vue # Карточка товара
│   │   │
│   │   ├── views/               # Страницы приложения
│   │   │   ├── HomePage.vue    # Главная (каталог)
│   │   │   ├── ProductDetailPage.vue  # Детали товара
│   │   │   └── CartPage.vue    # Страница корзины
│   │   │
│   │   ├── stores/              # Pinia stores (State Management)
│   │   │   ├── cart.js         # Store корзины
│   │   │   └── products.js     # Store товаров
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
│   ├── Dockerfile               # Docker образ frontend
│   ├── nginx.conf               # Конфигурация Nginx для SPA
│   ├── package.json             # NPM зависимости
│   └── vite.config.js          # Конфигурация Vite
│
├── nginx/                        # Reverse proxy конфигурация
│   └── nginx.conf               # Главная конфигурация Nginx
│
├── docker-compose.yml            # Оркестрация Docker контейнеров
|
└── README.md                     # Документация проекта
```

### 🔍 Назначение компонентов

#### Backend (FastAPI)

|Компонент|Назначение|
|---|---|
|**models/**|SQLAlchemy модели для работы с БД (ORM)|
|**schemas/**|Pydantic схемы для валидации входящих/исходящих данных|
|**repositories/**|Инкапсуляция логики работы с БД (Repository Pattern)|
|**services/**|Бизнес-логика приложения (Service Layer)|
|**routes/**|HTTP endpoints и маршрутизация (Controllers)|
|**config.py**|Настройки приложения (CORS, DB, пути)|
|**database.py**|Конфигурация SQLAlchemy и управление сессиями|
|**main.py**|Инициализация FastAPI, подключение middleware и роутеров|

#### Frontend (Vue.js 3)

|Компонент|Назначение|
|---|---|
|**components/**|Переиспользуемые UI компоненты|
|**views/**|Страницы приложения (роутинг)|
|**stores/**|Глобальное состояние приложения (Pinia)|
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

### Frontend

- **Vue.js** 3.5.22 - прогрессивный JavaScript фреймворк
- **Pinia** 3.0.3 - официальный state management для Vue 3
- **Vue Router** 4.5.1 - роутинг для SPA
- **Axios** 1.12.2 - HTTP клиент
- **Tailwind CSS** - utility-first CSS фреймворк
- **Vite** 7.1.7 - быстрый build tool

### DevOps

- **Docker** - контейнеризация приложений
- **Docker Compose** - оркестрация multi-container приложений
- **Nginx** - reverse proxy и веб-сервер

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
      "price": 299.99,
      "category_id": 1,
      "image_url": "https://...",
      "created_at": "2024-01-15T10:30:00",
      "category": {
        "id": 1,
        "name": "Electronics",
        "slug": "electronics"
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


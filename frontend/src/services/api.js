// frontend/src/services/api.js
/**
 * API сервис для взаимодействия с backend.
 * Централизует все HTTP запросы к FastAPI серверу.
 * Использует axios для выполнения запросов.
 */

import axios from 'axios'

// Базовый URL API из переменных окружения или значение по умолчанию
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

// Ключ для хранения JWT токена в localStorage
const TOKEN_STORAGE_KEY = 'auth_token'

// Создаем экземпляр axios с настройками по умолчанию
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Перехватчик запросов: подставляем JWT токен в заголовок Authorization
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_STORAGE_KEY)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

/**
 * API методы для работы с товарами
 */
export const productsAPI = {
  /**
   * Получить все товары
   */
  getAll() {
    return apiClient.get('/products')
  },

  /**
   * Получить товар по ID
   */
  getById(id) {
    return apiClient.get(`/products/${id}`)
  },

  /**
   * Получить товары по категории
   */
  getByCategory(categoryId) {
    return apiClient.get(`/products/category/${categoryId}`)
  },
}

/**
 * API методы для работы с категориями
 */
export const categoriesAPI = {
  /**
   * Получить все категории
   */
  getAll() {
    return apiClient.get('/categories')
  },

  /**
   * Получить категорию по ID
   */
  getById(id) {
    return apiClient.get(`/categories/${id}`)
  },
}

/**
 * API методы для работы с корзиной
 */
export const cartAPI = {
  /**
   * Добавить товар в корзину
   */
  addItem(item, cartData) {
    return apiClient.post('/cart/add', {
      product_id: item.product_id,
      quantity: item.quantity,
      cart: cartData,
    })
  },

  /**
   * Получить содержимое корзины
   */
  getCart(cartData) {
    return apiClient.post('/cart', cartData)
  },

  /**
   * Обновить количество товара
   */
  updateItem(item, cartData) {
    return apiClient.put('/cart/update', {
      product_id: item.product_id,
      quantity: item.quantity,
      cart: cartData,
    })
  },

  /**
   * Удалить товар из корзины
   */
  removeItem(productId, cartData) {
    return apiClient.delete(`/cart/remove/${productId}`, {
      data: {
        cart: cartData,
      },
    })
  },
}

/**
 * API методы для аутентификации
 */
export const authAPI = {
  /**
   * Зарегистрировать нового пользователя
   */
  register(email, password) {
    return apiClient.post('/auth/register', { email, password })
  },

  /**
   * Войти в аккаунт.
   * Backend ожидает данные формы (OAuth2PasswordRequestForm),
   * поэтому отправляем application/x-www-form-urlencoded с полями username/password.
   */
  login(email, password) {
    const params = new URLSearchParams()
    params.append('username', email)
    params.append('password', password)
    return apiClient.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  },

  /**
   * Подтвердить почту кодом из письма
   */
  verify(email, code) {
    return apiClient.post('/auth/verify', { email, code })
  },

  /**
   * Запросить повторную отправку кода подтверждения
   */
  resendCode(email) {
    return apiClient.post('/auth/resend-code', { email })
  },
}

export { TOKEN_STORAGE_KEY }

export default apiClient

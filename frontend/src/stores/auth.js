// frontend/src/stores/auth.js
/**
 * Pinia store для управления аутентификацией.
 * Хранит JWT токен и email пользователя в localStorage.
 * Следует принципу Single Responsibility - отвечает только за логику авторизации.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI, TOKEN_STORAGE_KEY } from '@/services/api'

const EMAIL_STORAGE_KEY = 'auth_email'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref(localStorage.getItem(TOKEN_STORAGE_KEY) || null)
  const email = ref(localStorage.getItem(EMAIL_STORAGE_KEY) || null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)

  // Actions
  /**
   * Войти в аккаунт по email и паролю
   */
  async function login(userEmail, password) {
    const response = await authAPI.login(userEmail, password)
    token.value = response.data.access_token
    email.value = userEmail
    localStorage.setItem(TOKEN_STORAGE_KEY, token.value)
    localStorage.setItem(EMAIL_STORAGE_KEY, userEmail)
  }

  /**
   * Зарегистрировать нового пользователя.
   * Вход НЕ выполняется — сначала нужно подтвердить почту кодом.
   * Возвращает данные ответа (в т.ч. telegram_link, если бот настроен).
   */
  async function register(userEmail, password) {
    const response = await authAPI.register(userEmail, password)
    return response.data
  }

  /**
   * Подтвердить почту кодом и войти
   */
  async function verify(userEmail, code) {
    const response = await authAPI.verify(userEmail, code)
    token.value = response.data.access_token
    email.value = userEmail
    localStorage.setItem(TOKEN_STORAGE_KEY, token.value)
    localStorage.setItem(EMAIL_STORAGE_KEY, userEmail)
  }

  /**
   * Запросить повторную отправку кода подтверждения
   */
  async function resendCode(userEmail) {
    await authAPI.resendCode(userEmail)
  }

  /**
   * Выйти из аккаунта
   */
  function logout() {
    token.value = null
    email.value = null
    localStorage.removeItem(TOKEN_STORAGE_KEY)
    localStorage.removeItem(EMAIL_STORAGE_KEY)
  }

  return {
    // State
    token,
    email,
    // Getters
    isAuthenticated,
    // Actions
    login,
    register,
    verify,
    resendCode,
    logout,
  }
})

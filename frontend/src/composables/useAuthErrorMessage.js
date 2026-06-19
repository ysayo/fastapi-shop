// frontend/src/composables/useAuthErrorMessage.js
/**
 * Composable для превращения ошибки axios в понятное локализованное сообщение
 * на страницах входа/регистрации.
 */

import { useI18n } from 'vue-i18n'

export function useAuthErrorMessage() {
  const { t } = useI18n()

  /**
   * @param {object} err - ошибка axios
   * @param {boolean} isLogin - true для входа, false для регистрации
   * @returns {string} сообщение для пользователя
   */
  return (err, isLogin) => {
    // Сервер не ответил (нет соединения / CORS / сервер не запущен)
    if (!err.response) {
      return t('auth.errors.network')
    }

    const status = err.response.status
    const detail = err.response.data?.detail

    // 422 — ошибка валидации (например, неверный формат email)
    if (status === 422) {
      return t('auth.errors.validation')
    }

    // Распознаём известные текстовые ответы бэкенда
    if (typeof detail === 'string') {
      if (/already registered/i.test(detail)) {
        return t('auth.errors.emailExists')
      }
      if (/incorrect email or password|no registered user/i.test(detail)) {
        return t('auth.errors.invalidCredentials')
      }
      if (/invalid verification code/i.test(detail)) {
        return t('auth.errors.invalidCode')
      }
      if (/verification code expired/i.test(detail)) {
        return t('auth.errors.codeExpired')
      }
      if (/already verified/i.test(detail)) {
        return t('auth.errors.alreadyVerified')
      }
    }

    // Ошибка на стороне сервера
    if (status >= 500) {
      return t('auth.errors.server')
    }

    // Если бэкенд прислал понятный текст — показываем его, иначе общий фолбэк
    if (typeof detail === 'string' && detail.trim()) {
      return detail
    }
    return isLogin ? t('auth.errors.loginFailed') : t('auth.errors.registerFailed')
  }
}

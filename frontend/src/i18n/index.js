// frontend/src/i18n/index.js
/**
 * Настройка интернационализации (vue-i18n).
 * Поддерживает русский и английский языки, выбор сохраняется в localStorage.
 */

import { createI18n } from 'vue-i18n'
import en from './locales/en.js'
import ru from './locales/ru.js'

const LOCALE_STORAGE_KEY = 'locale'
const SUPPORTED_LOCALES = ['ru', 'en']
const DEFAULT_LOCALE = 'ru'

/**
 * Определить начальный язык: из localStorage или по умолчанию
 */
function getInitialLocale() {
  const saved = localStorage.getItem(LOCALE_STORAGE_KEY)
  return SUPPORTED_LOCALES.includes(saved) ? saved : DEFAULT_LOCALE
}

const i18n = createI18n({
  legacy: false, // используем Composition API
  locale: getInitialLocale(),
  fallbackLocale: 'en',
  messages: { en, ru },
  // Правило множественного числа для русского языка (1 товар / 2 товара / 5 товаров)
  pluralRules: {
    ru: (choice) => {
      if (choice === 0) return 2
      const teen = choice % 100 >= 11 && choice % 100 <= 14
      const endsWithOne = choice % 10 === 1
      const endsWithTwoToFour = choice % 10 >= 2 && choice % 10 <= 4
      if (!teen && endsWithOne) return 0
      if (!teen && endsWithTwoToFour) return 1
      return 2
    },
  },
})

// Выставить атрибут lang у <html> при старте
document.documentElement.setAttribute('lang', i18n.global.locale.value)

/**
 * Сменить язык интерфейса и сохранить выбор
 */
export function setLocale(locale) {
  if (!SUPPORTED_LOCALES.includes(locale)) return
  i18n.global.locale.value = locale
  localStorage.setItem(LOCALE_STORAGE_KEY, locale)
  document.documentElement.setAttribute('lang', locale)
}

export { SUPPORTED_LOCALES }
export default i18n

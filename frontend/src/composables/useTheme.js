// frontend/src/composables/useTheme.js
/**
 * Управление темой оформления (светлая / тёмная).
 *
 * Тема хранится в localStorage и применяется добавлением класса `dark`
 * на <html> (Tailwind darkMode: 'class'). Состояние общее на всё приложение
 * (модульный ref), поэтому переключатель и любые другие компоненты синхронны.
 */
import { ref } from 'vue'

const THEME_KEY = 'theme'

// Общий реактивный флаг тёмной темы
const isDark = ref(false)

/** Применить тему: переключить класс на <html> и сохранить выбор. */
function apply(dark) {
  isDark.value = dark
  document.documentElement.classList.toggle('dark', dark)
  localStorage.setItem(THEME_KEY, dark ? 'dark' : 'light')
}

/**
 * Инициализация при старте приложения: берём сохранённый выбор,
 * иначе — системное предпочтение.
 */
export function initTheme() {
  const saved = localStorage.getItem(THEME_KEY)
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  isDark.value = saved ? saved === 'dark' : prefersDark
  // Класс уже мог быть выставлен инлайн-скриптом в index.html — синхронизируем.
  document.documentElement.classList.toggle('dark', isDark.value)
}

export function useTheme() {
  function toggle() {
    apply(!isDark.value)
  }
  return { isDark, toggle }
}

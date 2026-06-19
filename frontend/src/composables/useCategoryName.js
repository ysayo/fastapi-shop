// frontend/src/composables/useCategoryName.js
/**
 * Composable для перевода названия категории по её slug.
 * Если перевод для slug не найден — возвращает исходное имя из БД.
 */

import { useI18n } from 'vue-i18n'

export function useCategoryName() {
  const { t, te } = useI18n()

  return (category) => {
    if (!category) return ''
    const key = `categoryNames.${category.slug}`
    return te(key) ? t(key) : category.name
  }
}

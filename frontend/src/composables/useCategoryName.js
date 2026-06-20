// frontend/src/composables/useCategoryName.js
/**
 * Composable для перевода названия категории по её slug.
 * Если перевод для slug не найден — возвращает исходное имя из БД.
 */

import { useI18n } from 'vue-i18n'

export function useCategoryName() {
  const { t, te, locale } = useI18n()

  return (category) => {
    if (!category) return ''
    // 1) Локализованное название из БД (если переведено)
    const fromDb = category[`name_${locale.value}`]
    if (fromDb) return fromDb
    // 2) Фолбэк на маппинг по slug из locale-файлов (на время, пока БД не переведена)
    const key = `categoryNames.${category.slug}`
    if (te(key)) return t(key)
    // 3) Базовое имя из БД
    return category.name
  }
}

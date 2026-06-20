// frontend/src/composables/useLocalized.js
/**
 * Composable для выбора локализованного поля объекта из БД.
 *
 * Бэкенд отдаёт поля вида name_ru/name_en, description_ru/description_en.
 * Здесь выбираем версию под текущий язык интерфейса с фолбэком:
 *   <field>_<locale>  →  <field>_en  →  <field> (базовое поле).
 *
 * Так переключение языка происходит мгновенно, без перезапроса к API.
 */
import { useI18n } from 'vue-i18n'

export function useLocalized() {
  const { locale } = useI18n()

  return (obj, field) => {
    if (!obj) return ''
    return obj[`${field}_${locale.value}`] || obj[`${field}_en`] || obj[field] || ''
  }
}

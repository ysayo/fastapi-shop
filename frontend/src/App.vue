<!-- frontend/src/App.vue -->
<!--
  Корневой компонент приложения.
  Содержит общую структуру с Header и RouterView.
-->

<template>
  <div id="app" class="min-h-screen flex flex-col bg-ink-50 text-ink-900 dark:bg-ink-950 dark:text-ink-100 transition-colors">
    <!-- Шапка сайта -->
    <Header />

    <!-- Основной контент (роутер) -->
    <main class="flex-1">
      <RouterView />
    </main>

    <!-- Футер -->
    <footer class="mt-20 border-t border-ink-200 bg-white dark:border-ink-800 dark:bg-ink-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div class="flex flex-col items-center gap-3 text-center">
          <div class="flex items-center gap-2">
            <span
              class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 text-white shadow-glow"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
            </span>
            <span class="text-lg font-bold text-ink-900 dark:text-ink-50">FastAPI Shop</span>
          </div>
          <p class="text-ink-600 dark:text-ink-300">{{ t('footer.rights') }}</p>
          <p class="text-sm text-ink-400 dark:text-ink-500">{{ t('footer.builtWith') }}</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterView, useRoute } from 'vue-router'
import Header from '@/components/Header.vue'
import { useCartStore } from '@/stores/cart'
import { initTheme } from '@/composables/useTheme'

const { t, locale } = useI18n()
const route = useRoute()
const cartStore = useCartStore()

// Применяем сохранённую тему (светлая/тёмная) при загрузке приложения
initTheme()

// Обновлять заголовок вкладки при смене языка на текущей странице
watch(locale, () => {
  if (route.meta.titleKey) {
    document.title = t(route.meta.titleKey)
  }
})

/**
 * Инициализация приложения
 */
onMounted(() => {
  // Загрузить корзину из localStorage при запуске
  cartStore.initCart()
})
</script>

<style scoped>
/* Убираем все переопределения стилей для #app */
/* Tailwind классы полностью контролируют layout */
</style>

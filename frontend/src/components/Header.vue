<!-- frontend/src/components/Header.vue -->
<!--
  Компонент шапки сайта.
  Содержит логотип, навигацию и счетчик товаров в корзине.
-->

<template>
  <header
    class="sticky top-0 z-50 border-b border-ink-200/70 bg-white/80 backdrop-blur-xl supports-[backdrop-filter]:bg-white/60 dark:border-ink-800/70 dark:bg-ink-900/80 dark:supports-[backdrop-filter]:bg-ink-900/60 transition-colors"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-20">
        <!-- Логотип -->
        <router-link to="/" class="flex items-center gap-2.5 group">
          <span
            class="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 text-white shadow-glow transition-transform duration-300 group-hover:scale-105 group-hover:-rotate-3"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
          </span>
          <span class="hidden sm:inline text-xl font-extrabold tracking-tight text-ink-900 dark:text-ink-50 whitespace-nowrap">FastAPI Shop</span>
        </router-link>

        <!-- Навигация -->
        <nav class="flex items-center gap-2 sm:gap-4">
          <!-- Ссылка на каталог -->
          <router-link
            to="/"
            class="hidden sm:inline-flex rounded-lg px-3 py-2 text-sm font-medium text-ink-600 hover:bg-ink-100 hover:text-ink-900 dark:text-ink-300 dark:hover:bg-ink-800 dark:hover:text-ink-50 transition-colors"
            active-class="!text-brand-700 !bg-brand-50 dark:!text-brand-300 dark:!bg-brand-500/10"
          >
            {{ t('nav.catalog') }}
          </router-link>

          <!-- Корзина -->
          <router-link
            to="/cart"
            class="relative inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-ink-600 hover:bg-ink-100 hover:text-ink-900 dark:text-ink-300 dark:hover:bg-ink-800 dark:hover:text-ink-50 transition-colors"
            active-class="!text-brand-700 !bg-brand-50 dark:!text-brand-300 dark:!bg-brand-500/10"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
            <span class="hidden sm:inline">{{ t('nav.cart') }}</span>

            <!-- Счетчик товаров -->
            <span
              v-if="cartStore.itemsCount > 0"
              class="absolute -top-1 -right-1 flex h-5 min-w-[20px] items-center justify-center rounded-full bg-gradient-to-br from-brand-500 to-brand-700 px-1 text-xs font-bold text-white shadow-glow"
            >
              {{ cartStore.itemsCount }}
            </span>
          </router-link>

          <!-- Переключатель темы -->
          <button
            type="button"
            class="inline-flex h-9 w-9 items-center justify-center rounded-lg text-ink-500 hover:bg-ink-100 hover:text-ink-900 dark:text-ink-300 dark:hover:bg-ink-800 dark:hover:text-ink-50 transition-colors"
            :aria-label="isDark ? t('theme.toLight') : t('theme.toDark')"
            :title="isDark ? t('theme.toLight') : t('theme.toDark')"
            @click="toggleTheme"
          >
            <!-- Луна (включить тёмную) -->
            <svg v-if="!isDark" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
              />
            </svg>
            <!-- Солнце (включить светлую) -->
            <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
          </button>

          <span class="hidden sm:block h-6 w-px bg-ink-200 dark:bg-ink-700"></span>

          <!-- Аккаунт: вход/регистрация или email + выход -->
          <template v-if="authStore.isAuthenticated">
            <span class="hidden lg:inline text-sm font-medium text-ink-500 dark:text-ink-400">{{ authStore.email }}</span>
            <button
              class="inline-flex items-center rounded-lg border border-ink-200 px-4 py-2 text-sm font-semibold text-ink-700 hover:border-ink-300 hover:bg-ink-50 dark:border-ink-700 dark:text-ink-200 dark:hover:bg-ink-800 transition-colors"
              @click="authStore.logout()"
            >
              {{ t('nav.logout') }}
            </button>
          </template>
          <router-link
            v-else
            to="/login"
            class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-br from-brand-600 to-brand-700 px-4 py-2 text-sm font-semibold text-white shadow-glow hover:from-brand-500 hover:to-brand-600 transition-all hover:-translate-y-0.5"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
            <span>{{ t('nav.signIn') }}</span>
          </router-link>

          <!-- Переключатель языка -->
          <LanguageSwitcher />
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import { useTheme } from '@/composables/useTheme'

const { t } = useI18n()
const cartStore = useCartStore()
const authStore = useAuthStore()
const { isDark, toggle: toggleTheme } = useTheme()
</script>

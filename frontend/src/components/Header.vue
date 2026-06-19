<!-- frontend/src/components/Header.vue -->
<!--
  Компонент шапки сайта.
  Содержит логотип, навигацию и счетчик товаров в корзине.
-->

<template>
  <header class="bg-white border-b-2 border-black sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex items-center justify-between h-20">
        <!-- Логотип -->
        <router-link to="/" class="flex items-center space-x-2 group">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-8 w-8 group-hover:scale-110 transition-transform"
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
          <span class="text-2xl font-bold text-black">FastAPI Shop</span>
        </router-link>

        <!-- Навигация -->
        <nav class="flex items-center space-x-8">
          <!-- Ссылка на каталог -->
          <router-link
            to="/"
            class="text-gray-700 hover:text-black transition-colors font-medium"
            active-class="text-black font-semibold"
          >
            {{ t('nav.catalog') }}
          </router-link>

          <!-- Корзина -->
          <router-link
            to="/cart"
            class="relative flex items-center space-x-2 text-gray-700 hover:text-black transition-colors font-medium"
            active-class="text-black font-semibold"
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
            <span>{{ t('nav.cart') }}</span>

            <!-- Счетчик товаров -->
            <span
              v-if="cartStore.itemsCount > 0"
              class="absolute -top-2 -right-2 bg-black text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center"
            >
              {{ cartStore.itemsCount }}
            </span>
          </router-link>

          <!-- Аккаунт: вход/регистрация или email + выход -->
          <template v-if="authStore.isAuthenticated">
            <span class="text-gray-700 font-medium hidden sm:inline">{{ authStore.email }}</span>
            <button
              class="border-2 border-black text-black px-4 py-2 rounded-md font-semibold hover:bg-black hover:text-white transition-colors"
              @click="authStore.logout()"
            >
              {{ t('nav.logout') }}
            </button>
          </template>
          <router-link
            v-else
            to="/login"
            class="flex items-center space-x-2 bg-black text-white px-4 py-2 rounded-md font-semibold hover:bg-gray-800 transition-colors"
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

const { t } = useI18n()
const cartStore = useCartStore()
const authStore = useAuthStore()
</script>

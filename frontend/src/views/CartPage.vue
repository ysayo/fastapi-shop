<!-- frontend/src/views/CartPage.vue -->
<!--
  Страница корзины покупок.
  Отображает список товаров в корзине с возможностью управления количеством.
-->

<template>
  <div class="min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Заголовок -->
      <div class="mb-10">
        <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-ink-900 mb-2">
          {{ t('cart.title') }}
        </h1>
        <p class="text-lg text-ink-500">{{ t('cart.subtitle') }}</p>
      </div>

      <!-- Состояние загрузки -->
      <div v-if="cartStore.loading" class="flex flex-col items-center py-20">
        <div class="h-14 w-14 animate-spin rounded-full border-4 border-ink-200 border-t-brand-600"></div>
        <p class="mt-4 text-lg text-ink-500">{{ t('cart.loading') }}</p>
      </div>

      <!-- Пустая корзина -->
      <div
        v-else-if="!cartStore.hasItems"
        class="flex flex-col items-center rounded-3xl border border-dashed border-ink-200 bg-white py-20 text-center"
      >
        <div class="flex h-24 w-24 items-center justify-center rounded-3xl bg-ink-100">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-12 w-12 text-ink-400"
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
        </div>
        <h2 class="mt-6 text-2xl font-bold text-ink-900 mb-2">{{ t('cart.empty') }}</h2>
        <p class="text-lg text-ink-500 mb-8">{{ t('cart.emptyHint') }}</p>
        <router-link
          to="/"
          class="inline-flex items-center rounded-xl bg-gradient-to-br from-brand-600 to-brand-700 py-3 px-8 text-base font-semibold text-white shadow-glow transition-all hover:from-brand-500 hover:to-brand-600 hover:-translate-y-0.5"
        >
          {{ t('cart.continueShopping') }}
        </router-link>
      </div>

      <!-- Содержимое корзины -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Список товаров -->
        <div class="lg:col-span-2 space-y-4">
          <CartItem
            v-for="item in cartStore.cartDetails?.items"
            :key="item.product_id"
            :item="item"
          />
        </div>

        <!-- Итоговая информация -->
        <div class="lg:col-span-1">
          <div class="rounded-2xl border border-ink-200/70 bg-white p-8 shadow-soft sticky top-24">
            <h2 class="text-xl font-bold text-ink-900 mb-6">{{ t('cart.orderSummary') }}</h2>

            <!-- Детали заказа -->
            <div class="space-y-4 mb-6">
              <div class="flex justify-between text-ink-600">
                <span>{{ t('cart.items', { count: cartStore.cartDetails?.items_count }) }}</span>
                <span class="font-medium text-ink-900">${{ cartStore.totalPrice.toFixed(2) }}</span>
              </div>

              <div class="flex justify-between text-ink-600">
                <span>{{ t('cart.shipping') }}</span>
                <span class="font-semibold text-emerald-600">{{ t('cart.free') }}</span>
              </div>

              <div class="border-t border-ink-200 pt-4">
                <div class="flex items-baseline justify-between">
                  <span class="text-lg font-bold text-ink-900">{{ t('cart.total') }}</span>
                  <span class="text-2xl font-extrabold tracking-tight text-ink-900">
                    ${{ cartStore.totalPrice.toFixed(2) }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Кнопка оформления заказа -->
            <button
              class="w-full rounded-xl bg-gradient-to-br from-brand-600 to-brand-700 py-3.5 px-6 text-base font-semibold text-white shadow-glow transition-all hover:from-brand-500 hover:to-brand-600 active:scale-[0.99] mb-3"
              @click="handleCheckout"
            >
              {{ t('cart.checkout') }}
            </button>

            <!-- Кнопка продолжить покупки -->
            <router-link
              to="/"
              class="block w-full rounded-xl bg-ink-100 py-3.5 px-6 text-base font-semibold text-ink-700 transition-colors hover:bg-ink-200 text-center"
            >
              {{ t('cart.continueShopping') }}
            </router-link>

            <!-- Кнопка очистить корзину -->
            <button
              @click="handleClearCart"
              class="w-full mt-5 text-sm font-medium text-red-500 transition-colors hover:text-red-600"
            >
              {{ t('cart.clearCart') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useCartStore } from '@/stores/cart'
import CartItem from '@/components/CartItem.vue'

const { t } = useI18n()
const cartStore = useCartStore()

/**
 * Оформление заказа (placeholder)
 */
function handleCheckout() {
  alert(t('cart.checkoutAlert'))
}

/**
 * Очистить корзину с подтверждением
 */
function handleClearCart() {
  if (confirm(t('cart.clearConfirm'))) {
    cartStore.clearCart()
  }
}

/**
 * Загрузить данные корзины при монтировании
 */
onMounted(async () => {
  await cartStore.fetchCartDetails()
})
</script>

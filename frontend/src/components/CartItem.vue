<!-- frontend/src/components/CartItem.vue -->
<!--
  Компонент элемента корзины.
  Отображает товар в корзине с возможностью изменения количества и удаления.
-->

<template>
  <div
    class="rounded-2xl border border-ink-200/70 bg-white p-5 shadow-soft transition-all hover:shadow-card dark:border-ink-800 dark:bg-ink-900"
  >
    <div class="flex gap-5">
      <!-- Изображение товара -->
      <div class="h-24 w-24 flex-shrink-0 overflow-hidden rounded-xl bg-ink-100 dark:bg-ink-800">
        <img
          :src="item.image_url"
          :alt="item.name"
          class="h-full w-full object-cover"
          @error="handleImageError"
        />
      </div>

      <!-- Информация о товаре -->
      <div class="flex-grow">
        <h3 class="text-base font-semibold text-ink-900 dark:text-ink-50 mb-1">
          {{ item.name }}
        </h3>
        <p class="text-sm text-ink-500 dark:text-ink-400 mb-3">${{ item.price.toFixed(2) }} {{ t('cart.each') }}</p>

        <!-- Управление количеством -->
        <div class="flex items-center gap-4">
          <div class="flex items-center rounded-xl border border-ink-200 text-ink-700 dark:border-ink-700 dark:text-ink-200">
            <button
              @click="decreaseQuantity"
              :disabled="updating"
              class="rounded-l-xl px-2.5 py-2 hover:bg-ink-100 transition-colors disabled:opacity-50 dark:hover:bg-ink-800"
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
                  d="M20 12H4"
                />
              </svg>
            </button>

            <span class="px-4 py-2 font-semibold min-w-[44px] text-center text-ink-900 dark:text-ink-50">
              {{ item.quantity }}
            </span>

            <button
              @click="increaseQuantity"
              :disabled="updating"
              class="rounded-r-xl px-2.5 py-2 hover:bg-ink-100 transition-colors disabled:opacity-50 dark:hover:bg-ink-800"
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
                  d="M12 4v16m8-8H4"
                />
              </svg>
            </button>
          </div>

          <!-- Кнопка удаления -->
          <button
            @click="handleRemove"
            :disabled="updating"
            class="rounded-lg p-2 text-ink-400 transition-colors hover:bg-red-50 hover:text-red-500 disabled:opacity-50 dark:text-ink-500 dark:hover:bg-red-500/10 dark:hover:text-red-400"
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
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Сумма -->
      <div class="text-right">
        <p class="text-lg font-extrabold tracking-tight text-ink-900 dark:text-ink-50">${{ item.subtotal.toFixed(2) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useCartStore } from '@/stores/cart'

const { t } = useI18n()

// Props
const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

// State
const cartStore = useCartStore()
const updating = ref(false)

// Methods
/**
 * Увеличить количество товара
 */
async function increaseQuantity() {
  updating.value = true
  await cartStore.updateQuantity(props.item.product_id, props.item.quantity + 1)
  updating.value = false
}

/**
 * Уменьшить количество товара
 */
async function decreaseQuantity() {
  updating.value = true
  if (props.item.quantity > 1) {
    await cartStore.updateQuantity(props.item.product_id, props.item.quantity - 1)
  } else {
    await cartStore.removeFromCart(props.item.product_id)
  }
  updating.value = false
}

/**
 * Удалить товар из корзины
 */
async function handleRemove() {
  updating.value = true
  await cartStore.removeFromCart(props.item.product_id)
  updating.value = false
}

/**
 * Обработка ошибки загрузки изображения
 */
function handleImageError(event) {
  event.target.src = 'https://via.placeholder.com/100x100?text=No+Image'
}
</script>

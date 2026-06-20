<!-- frontend/src/components/ProductCard.vue -->
<!--
  Компонент карточки товара для отображения в каталоге.
  Показывает основную информацию о товаре и кнопку добавления в корзину.
-->

<template>
  <div
    class="group flex flex-col overflow-hidden rounded-2xl border border-ink-200/70 bg-white shadow-soft transition-all duration-300 hover:-translate-y-1 hover:shadow-card hover:border-brand-200 dark:border-ink-800 dark:bg-ink-900 dark:hover:border-brand-500/50"
  >
    <!-- Изображение товара -->
    <router-link :to="`/product/${product.id}`" class="relative block">
      <div class="flex aspect-square items-center justify-center overflow-hidden bg-white p-5">
        <img
          :src="product.image_url"
          :alt="product.name"
          class="max-h-full max-w-full object-contain transition-transform duration-500 ease-out group-hover:scale-105"
          @error="handleImageError"
        />
      </div>
      <!-- Категория -->
      <span
        class="absolute left-3 top-3 rounded-full bg-white/90 px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-brand-700 shadow-sm backdrop-blur dark:bg-ink-900/80 dark:text-brand-300"
      >
        {{ categoryName(product.category) }}
      </span>
    </router-link>

    <!-- Информация о товаре -->
    <div class="flex flex-1 flex-col p-5">
      <!-- Название товара -->
      <router-link :to="`/product/${product.id}`">
        <h3
          class="mb-3 line-clamp-2 text-base font-semibold text-ink-900 transition-colors group-hover:text-brand-700 dark:text-ink-50 dark:group-hover:text-brand-300"
        >
          {{ localized(product, 'name') }}
        </h3>
      </router-link>

      <!-- Цена -->
      <p class="mb-4 mt-auto text-2xl font-extrabold tracking-tight text-ink-900 dark:text-ink-50">
        ${{ product.price.toFixed(2) }}
      </p>

      <!-- Кнопка добавления в корзину -->
      <button
        @click="handleAddToCart"
        :disabled="adding"
        class="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-br from-brand-600 to-brand-700 py-3 px-4 text-sm font-semibold text-white shadow-glow transition-all hover:from-brand-500 hover:to-brand-600 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50"
      >
        <svg
          v-if="!adding"
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4"
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
        {{ adding ? t('product.adding') : t('product.addToCart') }}
      </button>

      <!-- Уведомление об успешном добавлении -->
      <transition name="fade">
        <div
          v-if="showNotification"
          class="mt-3 flex items-center justify-center gap-1.5 text-sm font-medium text-emerald-600"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          {{ t('product.addedToCart') }}
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useCartStore } from '@/stores/cart'
import { useCategoryName } from '@/composables/useCategoryName'
import { useLocalized } from '@/composables/useLocalized'

const { t } = useI18n()
const categoryName = useCategoryName()
const localized = useLocalized()

// Props
const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
})

// State
const cartStore = useCartStore()
const adding = ref(false)
const showNotification = ref(false)

/**
 * Добавить товар в корзину
 */
async function handleAddToCart() {
  adding.value = true
  const success = await cartStore.addToCart(props.product.id, 1)

  if (success) {
    showNotification.value = true
    setTimeout(() => {
      showNotification.value = false
    }, 2000)
  }

  adding.value = false
}

/**
 * Обработка ошибки загрузки изображения
 */
function handleImageError(event) {
  event.target.src = 'https://via.placeholder.com/400x400?text=No+Image'
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
